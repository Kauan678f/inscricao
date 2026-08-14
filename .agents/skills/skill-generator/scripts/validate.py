# /// script
# requires-python = ">=3.8"
# ///

"""
Validate an Agent Skill's structure and SKILL.md content.

Checks directory structure, frontmatter format, description length,
file references, and best-practice compliance.
"""

import argparse
import json
import os
import re
import sys
import textwrap


class ValidationResult:
    """Collects validation errors, warnings, and info messages."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_info(self, msg: str) -> None:
        self.info.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "info": len(self.info),
            },
        }


def parse_frontmatter(content: str) -> tuple:
    """Extract YAML frontmatter and body from SKILL.md content.

    Returns (frontmatter_dict, body_str) or (None, content) if no frontmatter.
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return None, content

    fm_text = match.group(1)
    body = match.group(2)

    # Simple YAML parsing for name and description
    fm = {}
    current_key = None
    current_value_lines = []

    for line in fm_text.split("\n"):
        # Check for key: value
        key_match = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if key_match:
            # Save previous key if any
            if current_key:
                fm[current_key] = " ".join(current_value_lines).strip()

            current_key = key_match.group(1)
            value = key_match.group(2).strip()
            if value == ">" or value == "|":
                current_value_lines = []
            else:
                current_value_lines = [value] if value else []
        elif current_key and line.startswith("  "):
            current_value_lines.append(line.strip())

    # Save last key
    if current_key:
        fm[current_key] = " ".join(current_value_lines).strip()

    return fm, body


def validate_skill(skill_path: str) -> ValidationResult:
    """Run all validation checks on a skill directory."""
    result = ValidationResult()
    skill_path = os.path.abspath(skill_path)
    skill_name = os.path.basename(skill_path)

    # Check SKILL.md exists
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md_path):
        result.error(f"SKILL.md not found at: {skill_md_path}")
        return result

    result.add_info(f"Skill path: {skill_path}")
    result.add_info(f"Skill name (from folder): {skill_name}")

    # Read SKILL.md
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check line count
    lines = content.split("\n")
    line_count = len(lines)
    result.add_info(f"SKILL.md line count: {line_count}")

    if line_count > 500:
        result.warn(
            f"SKILL.md has {line_count} lines (recommended: under 500). "
            f"Consider moving detailed content to references/."
        )

    # Estimate token count (rough: ~4 chars per token)
    char_count = len(content)
    estimated_tokens = char_count // 4
    result.add_info(f"Estimated token count: ~{estimated_tokens}")

    if estimated_tokens > 5000:
        result.warn(
            f"SKILL.md is ~{estimated_tokens} tokens (recommended: under 5,000). "
            f"Move detailed reference material to separate files."
        )

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        result.error(
            "No YAML frontmatter found. SKILL.md must start with '---' delimited frontmatter."
        )
        return result

    # Validate name field
    if "name" not in frontmatter:
        result.error("Frontmatter missing required field: 'name'")
    elif frontmatter["name"] != skill_name:
        result.error(
            f"Frontmatter 'name' ({frontmatter['name']}) does not match "
            f"folder name ({skill_name}). These must be identical."
        )
    else:
        result.add_info(f"Name field: {frontmatter['name']} ✓")

    # Validate description field
    if "description" not in frontmatter:
        result.error("Frontmatter missing required field: 'description'")
    else:
        desc = frontmatter["description"]
        desc_len = len(desc)
        result.add_info(f"Description length: {desc_len} characters")

        if desc_len > 1024:
            result.error(
                f"Description is {desc_len} characters (hard limit: 1024). "
                f"Shorten it."
            )

        if desc_len < 20:
            result.warn("Description is very short. A good description is 1-3 sentences.")

        # Check for TODO placeholders
        if "TODO" in desc:
            result.error("Description contains TODO placeholder. Replace with actual content.")

        # Check for imperative phrasing
        imperative_patterns = [
            r"use this skill",
            r"use when",
            r"activate when",
            r"invoke when",
        ]
        has_imperative = any(
            re.search(p, desc, re.IGNORECASE) for p in imperative_patterns
        )
        if not has_imperative:
            result.warn(
                "Description doesn't use imperative phrasing. "
                "Consider starting with 'Use this skill when...' for better triggering."
            )

    # Check body for TODO placeholders
    if "TODO" in body:
        result.warn("SKILL.md body contains TODO placeholders. Replace with actual content.")

    # Check for referenced scripts — skip example references inside code blocks
    # Extract references only from non-code-block sections
    non_code_content = re.sub(r"````[\s\S]*?````", "", content)  # 4-backtick blocks
    non_code_content = re.sub(r"```[\s\S]*?```", "", non_code_content)  # 3-backtick blocks
    non_code_content = re.sub(r"`[^`\n]+`", "", non_code_content)  # inline code
    # Remove lines that are clearly examples (✅, ❌, or "quoted" instructions)
    non_code_content = re.sub(r"^.*[✅❌].*$", "", non_code_content, flags=re.MULTILINE)
    non_code_content = re.sub(r'^.*"[^"]*references/[^"]*".*$', "", non_code_content, flags=re.MULTILINE)
    non_code_content = re.sub(r'^.*"[^"]*scripts/[^"]*".*$', "", non_code_content, flags=re.MULTILINE)
    script_refs = re.findall(r"scripts/([^\s\"'`()\-]+)", non_code_content)
    if script_refs:
        scripts_dir = os.path.join(skill_path, "scripts")
        for script_ref in set(script_refs):
            # Skip generic placeholders like <script-name>
            if "<" in script_ref or ">" in script_ref:
                continue
            script_path = os.path.join(scripts_dir, script_ref)
            if not os.path.exists(script_path):
                result.warn(
                    f"SKILL.md references 'scripts/{script_ref}' but file not found."
                )
            else:
                result.add_info(f"Script reference OK: scripts/{script_ref}")

    # Check for referenced files in references/ — skip example references
    ref_refs = re.findall(r"references/([^\s\"'`()\-]+)", non_code_content)
    if ref_refs:
        refs_dir = os.path.join(skill_path, "references")
        for ref_ref in set(ref_refs):
            if "<" in ref_ref or ">" in ref_ref:
                continue
            ref_path = os.path.join(refs_dir, ref_ref)
            if not os.path.exists(ref_path):
                result.warn(
                    f"SKILL.md references 'references/{ref_ref}' but file not found."
                )
            else:
                result.add_info(f"Reference file OK: references/{ref_ref}")

    # Check directory structure
    subdirs = [
        d
        for d in os.listdir(skill_path)
        if os.path.isdir(os.path.join(skill_path, d))
    ]
    if subdirs:
        result.add_info(f"Subdirectories found: {', '.join(sorted(subdirs))}")

    # Check scripts directory
    scripts_dir = os.path.join(skill_path, "scripts")
    if os.path.isdir(scripts_dir):
        scripts = [
            f
            for f in os.listdir(scripts_dir)
            if not f.startswith(".") and os.path.isfile(os.path.join(scripts_dir, f))
        ]
        if scripts:
            result.add_info(f"Scripts found: {', '.join(sorted(scripts))}")

            # Check each script for --help support
            for script in scripts:
                script_path = os.path.join(scripts_dir, script)
                with open(script_path, "r", encoding="utf-8") as f:
                    script_content = f.read()

                if "argparse" not in script_content and "--help" not in script_content:
                    result.warn(
                        f"scripts/{script} may not support --help. "
                        f"Scripts should include argument parsing with help text."
                    )

                # Check for interactive input() calls using regex
                # Match actual input() calls, not references inside strings or comments
                input_pattern = re.compile(
                    r"^(?![#\s]*[\"'])"
                    r"(?!.*[\"'].*input\()"
                    r".*\binput\s*\(",
                    re.MULTILINE,
                )
                # Simple heuristic: look for lines where input( appears
                # but is not inside a string literal or a comment
                has_interactive_input = False
                for line in script_content.split("\n"):
                    stripped = line.strip()
                    # Skip comments
                    if stripped.startswith("#"):
                        continue
                    # Skip string definitions that contain 'input('
                    if '"input("' in stripped or "'input('" in stripped:
                        continue
                    if '"input(" in' in stripped or "'input(' in" in stripped:
                        continue
                    # Check for actual input() call
                    if re.search(r"\binput\s*\(", stripped):
                        # Make sure it's not inside a string on this line
                        # Simple check: if quotes wrap around the match, skip it
                        if not re.search(r"[\"'].*\binput\s*\(.*[\"']", stripped):
                            has_interactive_input = True
                            break

                if has_interactive_input:
                    result.error(
                        f"scripts/{script} uses interactive input(). "
                        f"Scripts must not use interactive prompts — "
                        f"agents operate in non-interactive shells."
                    )

    # Check evals
    evals_path = os.path.join(skill_path, "evals", "evals.json")
    if os.path.exists(evals_path):
        try:
            with open(evals_path, "r", encoding="utf-8") as f:
                evals = json.load(f)

            eval_count = len(evals.get("evals", []))
            result.add_info(f"Eval test cases: {eval_count}")

            if eval_count < 2:
                result.warn("Consider adding at least 2-3 eval test cases.")

            # Check for TODO in evals
            evals_str = json.dumps(evals)
            if "TODO" in evals_str:
                result.warn("evals.json contains TODO placeholders.")

        except json.JSONDecodeError as e:
            result.error(f"evals/evals.json is not valid JSON: {e}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate an Agent Skill's structure and content.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Checks performed:
              - SKILL.md exists and has valid frontmatter
              - name field matches folder name
              - description is under 1024 characters
              - No TODO placeholders remain
              - Referenced scripts and files exist
              - Scripts don't use interactive input
              - Line count and token estimates

            Exit codes:
              0  All checks passed (may have warnings)
              1  Validation errors found
              2  Invalid arguments or skill path

            Examples:
              %(prog)s --skill-path .agents/skills/my-skill
              %(prog)s --skill-path ./csv-analyzer
        """),
    )
    parser.add_argument(
        "--skill-path",
        required=True,
        help="Path to the skill directory to validate",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.skill_path):
        print(
            f"Error: Not a directory: {args.skill_path}\n"
            f"Provide the path to the skill directory (containing SKILL.md).",
            file=sys.stderr,
        )
        sys.exit(2)

    result = validate_skill(args.skill_path)

    # Output structured results
    json.dump(result.to_dict(), sys.stdout, indent=2)
    print()

    # Print human-readable summary to stderr
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Validation {'PASSED ✓' if result.passed else 'FAILED ✗'}", file=sys.stderr)
    print(f"  Errors:   {len(result.errors)}", file=sys.stderr)
    print(f"  Warnings: {len(result.warnings)}", file=sys.stderr)

    if result.errors:
        print(f"\nErrors:", file=sys.stderr)
        for e in result.errors:
            print(f"  ✗ {e}", file=sys.stderr)

    if result.warnings:
        print(f"\nWarnings:", file=sys.stderr)
        for w in result.warnings:
            print(f"  ⚠ {w}", file=sys.stderr)

    print(f"{'='*50}", file=sys.stderr)

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()

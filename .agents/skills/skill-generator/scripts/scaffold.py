# /// script
# requires-python = ">=3.8"
# ///

"""
Scaffold a new Agent Skill directory structure.

Creates the appropriate directories and placeholder files based on
the skill type (simple, standard, or full).
"""

import argparse
import json
import os
import sys
import textwrap


SKILL_TYPES = {
    "simple": {
        "description": "Single SKILL.md with instructions only",
        "dirs": [],
        "files": ["SKILL.md"],
    },
    "standard": {
        "description": "SKILL.md + scripts/ directory with helper scripts",
        "dirs": ["scripts"],
        "files": ["SKILL.md"],
    },
    "full": {
        "description": "SKILL.md + scripts/ + references/ + assets/ + evals/",
        "dirs": ["scripts", "references", "assets", "evals", "evals/files"],
        "files": ["SKILL.md", "evals/evals.json"],
    },
}


def create_skill_md_placeholder(skill_path: str, name: str) -> None:
    """Create a placeholder SKILL.md with frontmatter."""
    content = textwrap.dedent(f"""\
        ---
        name: {name}
        description: >
          TODO: Write a description that tells the agent when to use this skill.
          Use imperative phrasing: "Use this skill when..."
          Focus on user intent, not implementation details.
          Stay under 1024 characters.
        ---

        # {name.replace('-', ' ').title()}

        TODO: Write the skill instructions here.

        ## Prerequisites

        - TODO: List required tools, runtimes, or environment setup.

        ## Workflow

        1. TODO: Step-by-step instructions.

        ## Gotchas

        - TODO: List non-obvious facts the agent would get wrong without being told.
    """)
    filepath = os.path.join(skill_path, "SKILL.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: SKILL.md", file=sys.stderr)


def create_evals_placeholder(skill_path: str, name: str) -> None:
    """Create a placeholder evals.json."""
    evals = {
        "skill_name": name,
        "evals": [
            {
                "id": 1,
                "prompt": f"TODO: Write a realistic user prompt that should trigger the {name} skill.",
                "expected_output": "TODO: Describe what success looks like.",
                "files": [],
                "assertions": [
                    "TODO: Add specific, verifiable assertions about the output."
                ],
            }
        ],
    }
    filepath = os.path.join(skill_path, "evals", "evals.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(evals, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Created: evals/evals.json", file=sys.stderr)


def create_gitkeep(dirpath: str, dirname: str) -> None:
    """Create a .gitkeep file in a directory to preserve it in version control."""
    gitkeep_path = os.path.join(dirpath, ".gitkeep")
    with open(gitkeep_path, "w", encoding="utf-8") as f:
        pass
    print(f"  Created: {dirname}/.gitkeep", file=sys.stderr)


def scaffold(name: str, skill_type: str, target: str) -> dict:
    """Create the skill directory structure and return a summary."""
    config = SKILL_TYPES[skill_type]
    skill_path = os.path.join(target, name) if not target.endswith(name) else target

    # Check if skill already exists
    if os.path.exists(skill_path):
        print(
            f"Error: Directory already exists: {skill_path}\n"
            f"Use a different name or remove the existing directory.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Create base directory
    os.makedirs(skill_path, exist_ok=True)
    print(f"Creating {skill_type} skill '{name}' at: {skill_path}", file=sys.stderr)

    # Create subdirectories
    created_dirs = []
    for d in config["dirs"]:
        dirpath = os.path.join(skill_path, d)
        os.makedirs(dirpath, exist_ok=True)
        created_dirs.append(d)
        print(f"  Created: {d}/", file=sys.stderr)
        # Add .gitkeep to empty dirs (except evals/files which gets .gitkeep anyway)
        if d not in ["evals/files"]:
            if d == "scripts" or d == "references" or d == "assets":
                create_gitkeep(dirpath, d)

    # Create placeholder files
    created_files = []
    for f in config["files"]:
        if f == "SKILL.md":
            create_skill_md_placeholder(skill_path, name)
            created_files.append("SKILL.md")
        elif f == "evals/evals.json":
            create_evals_placeholder(skill_path, name)
            created_files.append("evals/evals.json")

    # Add .gitkeep to evals/files if it exists
    evals_files_dir = os.path.join(skill_path, "evals", "files")
    if os.path.exists(evals_files_dir):
        create_gitkeep(evals_files_dir, "evals/files")

    result = {
        "status": "success",
        "skill_name": name,
        "skill_type": skill_type,
        "skill_path": os.path.abspath(skill_path),
        "created_dirs": created_dirs,
        "created_files": created_files,
        "next_steps": [
            f"Edit {os.path.join(skill_path, 'SKILL.md')} to add your skill instructions.",
        ],
    }

    if skill_type in ("standard", "full"):
        result["next_steps"].append(
            f"Add helper scripts to {os.path.join(skill_path, 'scripts/')}."
        )
    if skill_type == "full":
        result["next_steps"].extend([
            f"Add reference material to {os.path.join(skill_path, 'references/')}.",
            f"Add templates and assets to {os.path.join(skill_path, 'assets/')}.",
            f"Edit {os.path.join(skill_path, 'evals', 'evals.json')} to add test cases.",
        ])

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new Agent Skill directory structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Skill types:
              simple    Single SKILL.md with instructions only
              standard  SKILL.md + scripts/ directory
              full      SKILL.md + scripts/ + references/ + assets/ + evals/

            Examples:
              %(prog)s --name roll-dice --type simple
              %(prog)s --name csv-analyzer --type standard
              %(prog)s --name deploy-service --type full --target ./custom/skills/
        """),
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Skill name (lowercase, kebab-case, e.g. 'roll-dice')",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["simple", "standard", "full"],
        help="Skill complexity type",
    )
    parser.add_argument(
        "--target",
        default=".agents/skills",
        help="Target parent directory (default: .agents/skills)",
    )

    args = parser.parse_args()

    # Validate skill name
    if not args.name.replace("-", "").replace("_", "").isalnum():
        print(
            f"Error: Skill name must be alphanumeric with hyphens or underscores.\n"
            f"Received: '{args.name}'",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.name != args.name.lower():
        print(
            f"Error: Skill name must be lowercase.\n"
            f"Received: '{args.name}'. Did you mean '{args.name.lower()}'?",
            file=sys.stderr,
        )
        sys.exit(1)

    result = scaffold(args.name, args.type, args.target)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()

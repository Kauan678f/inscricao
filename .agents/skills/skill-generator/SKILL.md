---
name: skill-generator
description: >
  Generate new Agent Skills (SKILL.md files and supporting directories).
  Use this skill when the user asks to create, scaffold, generate, or build
  a new skill, agent skill, or SKILL.md — including when they describe a
  capability they want an agent to have and expect you to package it as a skill.
  Handles both simple skills (single SKILL.md) and complex skills with scripts,
  references, assets, templates, and eval scaffolding. Even if the user doesn't
  say "skill" explicitly, activate when they want to encapsulate reusable
  agent instructions into a portable format.
---

# Skill Generator

You are creating a new Agent Skill. Follow this workflow precisely.

## Language Rule

**All generated skills MUST be written in English.** This includes:
- The `name` and `description` fields in frontmatter
- All body content, section headings, and instructions in SKILL.md
- Script docstrings, help text, error messages, and comments
- Reference documentation and asset templates
- Eval prompts and assertions in evals.json

English is required because Agent Skills are a portable, open format designed to work across
any compatible agent. Writing in English ensures maximum compatibility, discoverability, and
reuse across teams, organizations, and the global skill ecosystem.

If the user describes the skill in another language, translate the concepts into English
for the skill content. You may explain the skill back to the user in their language,
but the generated files themselves must always be in English.

## Step 1: Gather Requirements

Ask the user (if not already clear from context):

1. **Skill name** — short, lowercase, kebab-case identifier (e.g. `csv-analyzer`, `deploy-service`).
2. **What the skill does** — the core capability in one paragraph.
3. **Target complexity** — determine from the user's description:
   - **Simple**: A single `SKILL.md` with instructions only. No scripts, no references.
   - **Standard**: `SKILL.md` + a `scripts/` directory with helper scripts.
   - **Full**: `SKILL.md` + `scripts/` + `references/` + `assets/` + `evals/` scaffolding.
4. **Target location** — default is `.agents/skills/<skill-name>/` relative to the project root. Ask if they want a different location.
5. **Operating systems** — which OS does the skill need to support? (bash, powershell, or both)
6. **Dependencies** — any external tools, libraries, or runtimes required.

If the user gives a vague description, use your judgment to determine complexity:
- If the skill only needs text instructions → **Simple**
- If it needs to run commands or automate steps → **Standard**
- If it involves multi-step workflows, validation, templates, or reference material → **Full**

## Step 2: Scaffold the Directory

Run the scaffold script to create the directory structure:

```bash
python scripts/scaffold.py --name "<skill-name>" --type <simple|standard|full> --target "<target-path>"
```

```powershell
python scripts/scaffold.py --name "<skill-name>" --type <simple|standard|full> --target "<target-path>"
```

The script creates the appropriate directories and placeholder files. If `--target` is omitted, it defaults to `.agents/skills/<skill-name>/`.

## Step 3: Write the SKILL.md

### Frontmatter

```yaml
---
name: <skill-name>
description: >
  <A 1-3 sentence description following these rules:>
  - Use imperative phrasing: "Use this skill when..."
  - Focus on user intent, not implementation details
  - List contexts where the skill applies, including non-obvious ones
  - Stay under 1024 characters
---
```

### Body Structure

Write the body following these principles:

1. **Add what the agent lacks, omit what it knows.** Don't explain HTTP, JSON, or common tools. Focus on project-specific conventions, non-obvious edge cases, and the particular tools/APIs to use.

2. **Aim for moderate detail.** Concise, stepwise guidance with a working example outperforms exhaustive documentation. Target under 500 lines / 5,000 tokens.

3. **Match specificity to fragility.** Be prescriptive for fragile operations (exact commands, specific sequences). Be flexible where multiple approaches are valid.

4. **Provide defaults, not menus.** Pick one recommended approach. Mention alternatives briefly.

5. **Favor procedures over declarations.** Teach methods, not specific answers.

### Body Sections (include as appropriate)

```markdown
# <Skill Title>

<Brief overview of what the skill does and when to use it.>

## Prerequisites
<List any required tools, runtimes, or environment setup.>

## Workflow
<Step-by-step numbered instructions. Include progress checklists for multi-step workflows.>

## Available Scripts
<List bundled scripts with brief descriptions. Reference with relative paths.>

## Gotchas
<List environment-specific facts that defy reasonable assumptions. Be concrete:>
- ❌ "Handle errors appropriately"
- ✅ "The /health endpoint returns 200 even if the DB is down. Use /ready instead."

## Validation
<Instructions to validate the skill's output before finalizing.>
```

### Cross-platform Commands

When providing terminal commands, always include both bash and powershell variants if the skill should support both:

````markdown
```bash
echo "Hello from bash"
```

```powershell
Write-Output "Hello from PowerShell"
```
````

## Step 4: Create Scripts (Standard and Full only)

For each script in `scripts/`:

1. **Use inline dependencies** (PEP 723 for Python, import maps for Deno, etc.)
2. **Include `--help` output** with description, flags, and examples
3. **Never use interactive prompts** — accept all input via flags, env vars, or stdin
4. **Use structured output** — JSON to stdout, diagnostics to stderr
5. **Be idempotent** — safe to run multiple times
6. **Include meaningful error messages** that say what went wrong, what was expected, and what to try
7. **Use distinct exit codes** for different failure types

### Script Template (Python)

```python
# /// script
# dependencies = [
#   "dependency1>=1.0",
# ]
# ///

"""Brief description of what this script does."""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Brief description",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.json
  %(prog)s --format csv --output result.csv input.json
        """,
    )
    parser.add_argument("input", help="Input file path")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format (default: json)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")

    args = parser.parse_args()

    # Script logic here
    result = {"status": "success"}

    # Structured output to stdout
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
```

## Step 5: Create References (Full only)

Place detailed reference material in `references/`. Tell the agent in SKILL.md **when** to load each file:

- ✅ `"Read references/api-errors.md if the API returns a non-200 status code"`
- ❌ `"See references/ for details"`

## Step 6: Create Assets (Full only)

Place templates, sample files, and other static resources in `assets/`.
Templates follow this pattern:

````markdown
# [Title]

## Section 1
[Description of what goes here]

## Section 2
[Description of what goes here]
````

## Step 7: Create Eval Scaffolding (Full only)

Create `evals/evals.json` with 2-3 starter test cases:

```json
{
  "skill_name": "<skill-name>",
  "evals": [
    {
      "id": 1,
      "prompt": "<realistic user prompt that should trigger the skill>",
      "expected_output": "<description of what success looks like>",
      "files": [],
      "assertions": [
        "<specific, verifiable assertion about the output>"
      ]
    }
  ]
}
```

**Tips for test cases:**
- Vary phrasing: formal, casual, with typos
- Mix terse and detailed prompts
- Include at least one edge case
- Use realistic context (file paths, column names, etc.)

## Step 8: Validate

Run the validation script to check the skill's structure and content:

```bash
python scripts/validate.py --skill-path "<path-to-skill>"
```

```powershell
python scripts/validate.py --skill-path "<path-to-skill>"
```

Fix any issues reported by the validator before presenting the skill to the user.

## Step 9: Present the Skill

Show the user:
1. The complete directory tree of the created skill
2. The full SKILL.md content
3. How to test it (e.g., suggested prompts to try)
4. Any next steps (refining the description, adding more evals, etc.)

## Gotchas

- The `name` field in frontmatter **must match** the folder name exactly.
- The `description` field has a **hard limit of 1024 characters**.
- SKILL.md should stay **under 500 lines / 5,000 tokens**. Move detailed content to `references/`.
- Script paths in SKILL.md are **relative to the skill directory root**.
- Agents operate in **non-interactive shells** — scripts must never block on TTY input.
- Always use **relative paths** from the skill directory root when referencing bundled files.
- **Progressive disclosure**: only the `name` and `description` are loaded at discovery time. The full body loads only when the skill activates. This means the description carries the entire burden of triggering.

# SKILL.md Format Specification

Read this document when you need exact details on the SKILL.md file format.

## File Structure

A skill is a folder containing a `SKILL.md` file. The standard location is `.agents/skills/<skill-name>/`.

```
<skill-name>/
├── SKILL.md              # Required — main instruction file
├── scripts/              # Optional — helper scripts
├── references/           # Optional — detailed reference material
├── assets/               # Optional — templates, samples, static resources
└── evals/                # Optional — evaluation test cases
    ├── evals.json
    └── files/            # Input files for test cases
```

## Frontmatter (YAML)

The file begins with YAML frontmatter delimited by `---`:

```yaml
---
name: <skill-name>
description: >
  <Up to 1024 characters describing when to use this skill>
---
```

### Required Fields

| Field         | Type   | Constraints        | Purpose                                           |
|---------------|--------|--------------------|----------------------------------------------------|
| `name`        | string | Must match folder  | Short identifier for the skill                     |
| `description` | string | Max 1024 chars     | Tells the agent when to activate this skill         |

### Optional Fields

| Field           | Type   | Purpose                                              |
|-----------------|--------|------------------------------------------------------|
| `compatibility` | string | Runtime/environment requirements (e.g., "node>=18")  |

## Body

Everything after the closing `---` is the body — the instructions the agent follows when the skill activates.

### Recommended Limits

- **Lines**: Under 500
- **Tokens**: Under 5,000 (~20,000 characters)

### Progressive Disclosure

At **discovery** time, the agent reads only `name` and `description`.
At **activation** time, the agent reads the full body.
For detailed reference material, use `references/` with explicit loading instructions.

## Script Conventions

Scripts in `scripts/` should:

1. Use inline dependency declarations (PEP 723 for Python)
2. Support `--help` with description, flags, and examples
3. Never use interactive prompts
4. Output structured data (JSON) to stdout
5. Send diagnostics to stderr
6. Be idempotent
7. Use distinct exit codes for different failure types

## Path Resolution

All paths in SKILL.md are relative to the skill directory root:

- `scripts/validate.sh` → `<skill-dir>/scripts/validate.sh`
- `references/api.md` → `<skill-dir>/references/api.md`
- `assets/template.md` → `<skill-dir>/assets/template.md`

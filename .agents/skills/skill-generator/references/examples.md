# Example Skills

Read this document for reference implementations at each complexity level.

---

## Simple Skill: `roll-dice`

**Structure:**
```
roll-dice/
└── SKILL.md
```

**SKILL.md:**
```markdown
---
name: roll-dice
description: >
  Roll dice using a random number generator. Use when asked to roll a die
  (d6, d20, etc.), roll dice, or generate a random dice roll.
---

To roll a die, use the following command that generates a random number
from 1 to the given number of sides:

` ``bash
echo $((RANDOM % <sides> + 1))
` ``

` ``powershell
Get-Random -Minimum 1 -Maximum (<sides> + 1)
` ``

Replace `<sides>` with the number of sides on the die (e.g., 6 for d6, 20 for d20).
```

**Why it works:**
- Clear, focused description triggers on dice-related queries
- Instructions are minimal — just the command to run
- Cross-platform support (bash + powershell)

---

## Standard Skill: `csv-analyzer`

**Structure:**
```
csv-analyzer/
├── SKILL.md
└── scripts/
    └── analyze.py
```

**SKILL.md:**
```markdown
---
name: csv-analyzer
description: >
  Analyze CSV and tabular data files — compute summary statistics, add derived
  columns, generate charts, and clean messy data. Use this skill when the user
  has a CSV, TSV, or Excel file and wants to explore, transform, or visualize
  the data, even if they don't explicitly mention "CSV" or "analysis."
---

# CSV Analyzer

## Workflow

1. Read the file to understand its structure:
   ` ``bash
   python scripts/analyze.py --preview <input-file>
   ` ``

2. Based on the user's request, run the appropriate analysis:
   ` ``bash
   python scripts/analyze.py --stats <input-file>
   python scripts/analyze.py --chart bar --columns "col1,col2" <input-file>
   python scripts/analyze.py --clean --output cleaned.csv <input-file>
   ` ``

3. Present results to the user with clear explanations.

## Available Scripts

- **scripts/analyze.py** — Core analysis tool. Run `python scripts/analyze.py --help` for options.

## Gotchas

- Excel files (.xlsx) require the `openpyxl` dependency. The script handles this automatically.
- Files over 100MB should use `--sample 10000` to avoid memory issues.
- Date columns are auto-detected but may need `--date-format` for non-standard formats.
```

**Why it works:**
- Description covers multiple file types and use cases
- Includes non-obvious trigger ("even if they don't explicitly mention CSV")
- Scripts do the heavy lifting; SKILL.md orchestrates
- Gotchas prevent real mistakes

---

## Full Skill: `deploy-service`

**Structure:**
```
deploy-service/
├── SKILL.md
├── scripts/
│   ├── deploy.py
│   ├── rollback.py
│   └── health_check.py
├── references/
│   ├── environments.md
│   └── troubleshooting.md
├── assets/
│   └── deploy-checklist.md
└── evals/
    ├── evals.json
    └── files/
        └── sample-config.yaml
```

**SKILL.md:**
```markdown
---
name: deploy-service
description: >
  Deploy, rollback, and manage service deployments to staging and production
  environments. Use this skill when asked to deploy code, release a version,
  roll back a deployment, or check deployment status. Also use when
  troubleshooting deployment failures or environment configuration issues.
---

# Deploy Service

## Prerequisites

- AWS CLI configured with appropriate credentials
- Docker installed and running
- Access to the container registry

## Workflow

- [ ] Step 1: Validate configuration
  ` ``bash
  python scripts/deploy.py --validate --config <config-file>
  ` ``

- [ ] Step 2: Build and tag the image
  ` ``bash
  python scripts/deploy.py --build --tag <version>
  ` ``

- [ ] Step 3: Deploy to target environment
  ` ``bash
  python scripts/deploy.py --deploy --env <staging|production> --tag <version>
  ` ``

- [ ] Step 4: Health check
  ` ``bash
  python scripts/health_check.py --env <environment> --timeout 120
  ` ``

- [ ] Step 5: Verify and report
  If health check fails, read references/troubleshooting.md for common fixes.
  If rollback is needed: `python scripts/rollback.py --env <environment>`

## Available Scripts

- **scripts/deploy.py** — Build, validate, and deploy services
- **scripts/rollback.py** — Roll back to the previous deployment
- **scripts/health_check.py** — Verify service health after deployment

## References

- Read **references/environments.md** when you need environment-specific configuration details.
- Read **references/troubleshooting.md** if a deployment fails or health check doesn't pass.

## Gotchas

- Production deploys require `--confirm` flag. The script will refuse without it.
- The `/health` endpoint returns 200 even if dependent services are down. Use `/ready`.
- Staging uses a different container registry than production. The script handles this.
- Rollback keeps the previous 3 versions. Anything older requires manual recovery.
```

**Why it works:**
- Checklist tracks multi-step workflow progress
- References load on demand (progressive disclosure)
- Scripts enforce safety (--confirm for production)
- Gotchas capture real operational knowledge
- Evals directory ready for systematic testing

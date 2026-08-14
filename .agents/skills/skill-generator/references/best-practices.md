# Best Practices for Skill Creation

Read this document when crafting skill instructions to ensure quality.

## Content Principles

### 1. Add What the Agent Lacks

Focus on project-specific conventions, non-obvious edge cases, and particular tools/APIs.
Don't explain common concepts (HTTP, JSON, databases).

**Ask yourself**: "Would the agent get this wrong without this instruction?" If no, cut it.

### 2. Moderate Detail

Concise, stepwise guidance + working example > exhaustive documentation.

### 3. Match Specificity to Fragility

- **Flexible tasks**: Explain *why*, let the agent choose *how*
- **Fragile tasks**: Prescribe exact commands and sequences

### 4. Defaults Over Menus

Pick one recommended approach. Mention alternatives briefly.

```markdown
<!-- Bad -->
You can use pypdf, pdfplumber, PyMuPDF, or pdf2image...

<!-- Good -->
Use pdfplumber for text extraction.
For scanned PDFs, use pdf2image with pytesseract instead.
```

### 5. Procedures Over Declarations

Teach reusable methods, not specific answers.

## High-Value Patterns

### Gotchas Sections

Concrete corrections to mistakes the agent would make:

```markdown
## Gotchas
- The users table uses soft deletes. Always add `WHERE deleted_at IS NULL`.
- `/health` returns 200 even if the DB is down. Use `/ready` instead.
```

### Progress Checklists

Track multi-step workflows:

```markdown
## Workflow
- [ ] Step 1: Analyze input
- [ ] Step 2: Transform data
- [ ] Step 3: Validate output
- [ ] Step 4: Generate report
```

### Validation Loops

Do work → validate → fix → repeat until clean:

```markdown
1. Make edits
2. Run: python scripts/validate.py output/
3. If validation fails, fix issues and re-validate
4. Proceed only when validation passes
```

### Plan-Validate-Execute

For batch/destructive operations:

1. Create a plan (structured format)
2. Validate against source of truth
3. Execute only after validation passes

### Output Templates

Provide concrete templates instead of describing format in prose.

## Description Writing

- **Imperative phrasing**: "Use this skill when…"
- **Focus on user intent**: What the user is trying to achieve
- **Be pushy**: Explicitly list applicable contexts
- **Concise**: 1-3 sentences, under 1024 characters
- **Include non-obvious triggers**: "even if they don't explicitly mention X"

## Script Design

- No interactive prompts (hard requirement)
- Support `--help`
- Structured output (JSON to stdout)
- Diagnostics to stderr
- Idempotent (safe to re-run)
- Meaningful error messages
- Distinct exit codes
- Pin dependency versions
- Safe defaults (require `--confirm` for destructive operations)

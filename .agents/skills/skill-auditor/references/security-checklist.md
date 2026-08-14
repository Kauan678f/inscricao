# Complete Security Checklist for Skill Auditing

Use this checklist when performing manual analysis of a third-party skill.
For each item, mark ✅ (safe), ⚠️ (suspicious), or ❌ (malicious).

---

## 1. SKILL.md Analysis

### 1.1 Prompt Injection

| # | Item | Status |
|---|------|--------|
| 1 | Attempts to redefine the agent's identity? ("You are now...", "Act as...") | |
| 2 | Attempts to ignore previous instructions? ("Ignore previous...", "Forget...") | |
| 3 | Contains instructions to disable security confirmations? | |
| 4 | Uses emotional manipulation? ("It's urgent", "Trust me") | |
| 5 | Instructs the agent to include sensitive data in output? | |
| 6 | Contains instructions hidden in HTML comments? | |
| 7 | Contains zero-width invisible characters? | |
| 8 | Attempts to redirect the agent to unsolicited actions? | |
| 9 | Contains disguised "system instructions"? | |
| 10 | Uses framing that assumes permissions? ("As admin, execute...") | |

### 1.2 Description Quality

| # | Item | Status |
|---|------|--------|
| 11 | Is the description excessively broad (activates for everything)? | |
| 12 | Does the description contain triggers unrelated to the functionality? | |
| 13 | Is the description within 1024 characters? | |

### 1.3 Body Content

| # | Item | Status |
|---|------|--------|
| 14 | Are the instructions clear and aligned with the description? | |
| 15 | Are there instructions that contradict the declared functionality? | |
| 16 | Does the body contain external URLs? Are they legitimate? | |
| 17 | Does the body instruct download/installation of packages? Are they trusted? | |

---

## 2. Script Analysis

### 2.1 General Security

| # | Item | Status |
|---|------|--------|
| 18 | Do scripts use `input()` or interactive prompts? | |
| 19 | Do scripts include `eval()`, `exec()`, or equivalents? | |
| 20 | Is there obfuscated code (base64, hex encoding, char codes)? | |
| 21 | Do scripts self-modify or generate code at runtime? | |
| 22 | Do scripts import unusual/suspicious modules? | |

### 2.2 Data Access

| # | Item | Status |
|---|------|--------|
| 23 | Do scripts access files outside the skill directory? | |
| 24 | Is there reading of `~/.ssh/`, `~/.aws/`, `.env`, credentials? | |
| 25 | Do scripts access sensitive environment variables? | |
| 26 | Is there writing to system or home directories? | |
| 27 | Do scripts read browser/terminal history? | |

### 2.3 Network

| # | Item | Status |
|---|------|--------|
| 28 | Do scripts make HTTP requests to external servers? | |
| 29 | Is there data sending via POST/PUT to external URLs? | |
| 30 | Is there a reverse shell pattern (sockets, netcat)? | |
| 31 | Do scripts perform unusual DNS lookups (possible DNS exfiltration)? | |
| 32 | Do URLs point to direct IPs instead of domains? | |

### 2.4 System

| # | Item | Status |
|---|------|--------|
| 33 | Do scripts modify `PATH`, `.bashrc`, `.zshrc`, or profiles? | |
| 34 | Is there creation of cron jobs, services, or scheduled tasks? | |
| 35 | Do scripts install packages from non-standard registries? | |
| 36 | Is there `curl | bash` or pipe-to-shell pattern? | |
| 37 | Do scripts use `sudo`, `runas`, or privilege escalation? | |
| 38 | Are there destructive operations (rm -rf, del, format, shred)? | |

### 2.5 Dependencies

| # | Item | Status |
|---|------|--------|
| 39 | Are inline dependencies (PEP 723) from well-known packages? | |
| 40 | Are dependency versions pinned? | |
| 41 | Does any dependency have a name similar to a popular package (typosquatting)? | |

---

## 3. References and Assets Analysis

| # | Item | Status |
|---|------|--------|
| 42 | Do reference files contain instructions disguised as documentation? | |
| 43 | Do templates in `assets/` inject code/instructions when used? | |
| 44 | Are there binary files that shouldn't be here? | |
| 45 | Are external links in references to legitimate domains? | |

---

## 4. Structural Analysis

| # | Item | Status |
|---|------|--------|
| 46 | Does the directory structure follow the expected pattern? | |
| 47 | Are there files in unexpected locations? | |
| 48 | Are there hidden files (dot files) that shouldn't exist? | |
| 49 | Does the frontmatter `name` match the folder name? | |
| 50 | Is there anything outside the declared scope of the skill? | |

---

## Note on False Positives

Not every match is malicious. Examples of legitimate false positives:

- A deployment skill may legitimately use `curl` to make requests.
- An analysis skill may need to read environment variables for configuration.
- A script may use `eval()` legitimately in controlled contexts (rare, but possible).

The key is: **does the action make sense for the skill's declared purpose?**
A skill that says "analyze CSVs" but reads `~/.ssh/id_rsa` is clearly malicious.

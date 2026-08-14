# /// script
# requires-python = ">=3.8"
# ///

"""
Security scanner for Agent Skills.

Scans SKILL.md files, scripts, references, and assets for security threats
including prompt injection, malicious code, data exfiltration, credential
harvesting, obfuscated code, and supply chain attacks.

Supports multilingual detection (English, Portuguese, Spanish).
"""

import argparse
import json
import os
import re
import sys
import textwrap
from pathlib import Path


# ============================================================================
# THREAT PATTERN DEFINITIONS
# ============================================================================

PROMPT_INJECTION_PATTERNS = [
    # Identity override (EN + PT + ES)
    {
        "id": "PI-001",
        "name": "Identity Override",
        "severity": "CRITICAL",
        "description": "Attempt to redefine the agent's identity or role",
        "patterns": [
            # English
            r"(?i)you\s+are\s+now\b",
            r"(?i)from\s+now\s+on\s+you\s+(are|will|must|should)",
            r"(?i)your\s+new\s+(role|identity|persona|purpose)\s+is",
            r"(?i)act\s+as\s+(if\s+you\s+are|a|an)\b",
            r"(?i)pretend\s+(to\s+be|you\s+are)",
            r"(?i)you\s+are\s+no\s+longer",
            r"(?i)switch\s+(to|into)\s+(a\s+)?(new\s+)?(role|mode|persona)",
            # Portuguese
            r"(?i)voc[eê]\s+(agora\s+)?[eé]\s+(um|uma|o|a)\b",
            r"(?i)a\s+partir\s+de\s+agora\s+voc[eê]\s+[eé]",
            r"(?i)seu\s+novo\s+(papel|role|identidade|prop[oó]sito)\s+[eé]",
            r"(?i)finja\s+(ser|que\s+[eé]|que\s+voc[eê])",
            r"(?i)aja\s+como\s+(se\s+fosse|um|uma)",
            r"(?i)voc[eê]\s+n[aã]o\s+[eé]\s+mais",
            r"(?i)mude\s+(para|seu)\s+(papel|modo|persona)",
            # Spanish
            r"(?i)ahora\s+(eres|sos)\b",
            r"(?i)a\s+partir\s+de\s+ahora\s+(eres|sos|ser[aá]s)",
            r"(?i)act[uú]a\s+como\s+(si\s+fueras|un|una)",
        ],
    },
    # Instruction override (EN + PT + ES)
    {
        "id": "PI-002",
        "name": "Instruction Override",
        "severity": "CRITICAL",
        "description": "Attempt to override or ignore previous instructions",
        "patterns": [
            # English
            r"(?i)ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions|rules|guidelines|constraints)",
            r"(?i)forget\s+(all\s+)?(previous|prior|above|earlier|everything|your)\b",
            r"(?i)disregard\s+(all\s+)?(previous|prior|above|the)\b",
            r"(?i)override\s+(all\s+)?(previous|prior|safety|security)\b",
            r"(?i)new\s+instructions?\s*[:\-]",
            r"(?i)updated?\s+instructions?\s*[:\-]",
            r"(?i)the\s+real\s+instructions?\s+(are|is)\b",
            r"(?i)system\s*prompt\s*[:\-]",
            # Portuguese
            r"(?i)ignore\s+(todas?\s+)?(as\s+)?(instru[cç][oõ]es|regras|diretrizes)\s+(anteriores|pr[eé]vias|acima)",
            r"(?i)esque[cç]a\s+(tudo|todas?\s+as|as\s+instru[cç][oõ]es|o\s+que)",
            r"(?i)desconsidere\s+(todas?\s+)?(as\s+)?(instru[cç][oõ]es|regras|orienta[cç][oõ]es)",
            r"(?i)novas?\s+instru[cç][oõ]es\s*[:\-]",
            r"(?i)instru[cç][oõ]es\s+atualizadas?\s*[:\-]",
            r"(?i)as\s+verdadeiras\s+instru[cç][oõ]es\s+(s[aã]o|[eé])",
            r"(?i)sobrescreva\s+(todas?\s+)?(as\s+)?(instru[cç][oõ]es|regras)",
            r"(?i)substitua\s+(todas?\s+)?(as\s+)?(instru[cç][oõ]es|regras)",
            # Spanish
            r"(?i)ignora\s+(todas?\s+)?(las\s+)?instrucciones\s+(anteriores|previas)",
            r"(?i)olvida\s+(todo|todas?\s+las|las\s+instrucciones)",
        ],
    },
    # Permission escalation (EN + PT + ES)
    {
        "id": "PI-003",
        "name": "Permission Escalation",
        "severity": "HIGH",
        "description": "Attempt to escalate permissions or disable security confirmations",
        "patterns": [
            # English
            r"(?i)(run|execute|do)\s+(this\s+)?(with(out)?|no)\s+(asking|confirmation|permission|approval)",
            r"(?i)auto[\-\s]?(approve|accept|confirm|run)",
            r"(?i)(skip|bypass|disable|turn\s+off)\s+(all\s+)?(safety|security|confirmation|verification|check|warning|prompt)",
            r"(?i)don'?t\s+(ask|wait|check|verify|confirm)",
            r"(?i)no\s+need\s+(to|for)\s+(ask|confirm|check|verify)",
            r"(?i)trust\s+(this|me|the\s+skill)",
            r"(?i)safe\s+to\s+auto[\-\s]?run",
            # Portuguese
            r"(?i)(execute|rode|fa[cç]a)\s+(isso\s+)?sem\s+(pedir|confirma[cç][aã]o|permiss[aã]o|perguntar)",
            r"(?i)(pule|ignore|desabilite|desative|desligue)\s+(todas?\s+)?(as\s+)?(verifica[cç][oõ]es|confirma[cç][oõ]es|seguran[cç]a|checagem)",
            r"(?i)n[aã]o\s+(precisa|[eé]\s+necess[aá]rio)\s+(pedir|confirmar|verificar|perguntar|checar)",
            r"(?i)confie\s+(nesta|nessa|neste|em\s+mim|na\s+skill)",
            r"(?i)n[aã]o\s+(pe[cç]a|pergunte|verifique|confirme|cheque)",
            r"(?i)seguro\s+para\s+(auto|executar\s+automaticamente)",
            # Spanish
            r"(?i)(ejecuta|haz)\s+(esto\s+)?sin\s+(pedir|confirmaci[oó]n|permiso|preguntar)",
            r"(?i)(salta|ignora|desactiva)\s+(todas?\s+)?(las\s+)?(verificaciones|confirmaciones|seguridad)",
            r"(?i)conf[ií]a\s+en\s+(esto|m[ií]|la\s+skill)",
        ],
    },
    # Social engineering (EN + PT + ES)
    {
        "id": "PI-004",
        "name": "Social Engineering / Manipulation",
        "severity": "HIGH",
        "description": "Emotional manipulation or social engineering attempt",
        "patterns": [
            # English
            r"(?i)(it'?s|this\s+is)\s+(very\s+)?(urgent|critical|emergency|important\s+that\s+you)",
            r"(?i)the\s+user\s+(wants|needs|asked|said)\s+(you\s+to\s+)?(ignore|skip|bypass|disable)",
            r"(?i)(I|we)\s+(am|are)\s+(your|the)\s+(creator|developer|admin|owner|master)",
            r"(?i)this\s+is\s+a\s+test\s*(,|\.\s)?\s*(just|so)\s+(do|run|execute)",
            r"(?i)(do|must|should|need\s+to)\s+keep\s+(this\s+)?(secret|hidden|private|confidential)",
            # Portuguese
            r"(?i)([eé]|isso\s+[eé])\s+(muito\s+)?(urgente|cr[ií]tico|emerg[eê]ncia|importante\s+que\s+voc[eê])",
            r"(?i)o\s+usu[aá]rio\s+(quer|precisa|pediu|disse)\s+(que\s+voc[eê]\s+)?(ignore|pule|desabilite|desative)",
            r"(?i)(eu|n[oó]s)\s+(sou|somos)\s+(seu|o|a)\s+(criador|desenvolvedor|admin|dono|mestre)",
            r"(?i)(isso|isto)\s+[eé]\s+um\s+teste\s*(,|\.)?\s*(apenas|s[oó])\s+(fa[cç]a|execute|rode)",
            r"(?i)(mantenha|guarde|deixe)\s+(isso\s+)?(em\s+)?(segredo|secreto|oculto|escondido|privado|confidencial)",
            # Spanish
            r"(?i)(es|esto\s+es)\s+(muy\s+)?(urgente|cr[ií]tico|emergencia|importante\s+que)",
            r"(?i)el\s+usuario\s+(quiere|necesita|pidi[oó])\s+(que\s+)?(ignores|saltes|desactives)",
        ],
    },
    # Data exfiltration via output (EN + PT)
    {
        "id": "PI-005",
        "name": "Data Exfiltration via Output",
        "severity": "CRITICAL",
        "description": "Instructions to include sensitive data in the agent's output",
        "patterns": [
            # English
            r"(?i)\b(include|add|append|insert|embed|encode)\b\s+.{0,40}\b(contents?\s+of|ssh\s+key|api.?key|token|password|secret|credential|\.env|private\s+key)\b",
            r"(?i)\b(read|cat|type|get)\b\s+.{0,20}(\.env\b|\.ssh/|\.aws/|\.npmrc|\.netrc|credentials?\b|secrets?\b|tokens?\b|passwords?\b)",
            r"(?i)\b(show|display|output|print|return)\b\s+.{0,30}\b(api[\-_\s]?key|secret\s+key|token|password|credential)\b",
            r"(?i)base64\s+(encode|encrypt)\s+.{0,30}(and|then)\s+(include|add|send|output)",
            # Portuguese
            r"(?i)\b(inclua|adicione|insira|coloque|embuta)\b\s+.{0,40}\b(conte[uú]do\s+d[eoa]|chave\s+ssh|chave\s+api|token|senha|segredo|credencia|\.env|chave\s+privada)\b",
            r"(?i)\b(leia|abra|mostre|exiba|imprima)\b\s+.{0,20}(\.env\b|\.ssh/|\.aws/|\.npmrc|credencia|segredo|token|senha)",
            r"(?i)\b(mostre|exiba|imprima|retorne|envie)\b\s+.{0,30}\b(chave\s+de?\s+api|chave\s+secreta|token|senha|credencia)\b",
        ],
    },
    # Hidden instructions (universal)
    {
        "id": "PI-006",
        "name": "Hidden Instructions",
        "severity": "CRITICAL",
        "description": "Instructions hidden in HTML comments, whitespace, or invisible characters",
        "patterns": [
            r"<!--\s*(?!slide).*?(instruction|instru[cç]|execute|run|ignore|forget|override|curl|wget|bash|python|powershell|esque[cç]|desconsider)",
            r"[\u200b\u200c\u200d\ufeff\u2060\u2061\u2062\u2063\u2064]",
        ],
    },
    # Action redirection (EN + PT)
    {
        "id": "PI-007",
        "name": "Action Redirection",
        "severity": "HIGH",
        "description": "Attempt to divert the agent to execute unrelated actions",
        "patterns": [
            # English
            r"(?i)before\s+(you\s+)?(do|start|begin|proceed).{0,40}(first|also|additionally)\s+(run|execute|do|send|curl|wget)",
            r"(?i)(also|additionally|while\s+you'?re\s+at\s+it|by\s+the\s+way).{0,40}(run|execute|send|curl|wget|download|install)",
            r"(?i)as\s+a\s+(side|bonus|extra)\s+(task|step|action)",
            # Portuguese
            r"(?i)antes\s+de\s+(come[cç]ar|fazer|iniciar|prosseguir).{0,40}(primeiro|tamb[eé]m|adicionalmente)\s+(rode|execute|fa[cç]a|envie|curl|wget)",
            r"(?i)(tamb[eé]m|adicionalmente|j[aá]\s+que\s+est[aá]|aproveitando).{0,40}(rode|execute|envie|curl|wget|baixe|instale)",
            r"(?i)como\s+(tarefa|etapa|a[cç][aã]o)\s+(extra|b[oô]nus|adicional|secund[aá]ria)",
        ],
    },
]

MALICIOUS_SCRIPT_PATTERNS = [
    # Reverse shells
    {
        "id": "MS-001",
        "name": "Reverse Shell",
        "severity": "CRITICAL",
        "description": "Attempt to open a reverse shell for remote access",
        "patterns": [
            r"bash\s+-i\s+>&\s*/dev/tcp/",
            r"nc\s+(-e|--exec)\s+",
            r"ncat\s+(-e|--exec)\s+",
            r"python[23]?\s+-c\s+['\"]import\s+socket",
            r"ruby\s+-rsocket\s+-e",
            r"perl\s+-e\s+['\"]use\s+Socket",
            r"php\s+-r\s+.*fsockopen",
            r"mkfifo\s+/tmp/",
            r"socat\s+exec:",
            r"New-Object\s+System\.Net\.Sockets\.TCPClient",
            r"Invoke-PowerShellTcp",
            r"\$client\s*=\s*New-Object\s+Net\.Sockets",
        ],
    },
    # Data exfiltration via network
    {
        "id": "MS-002",
        "name": "Network Data Exfiltration",
        "severity": "CRITICAL",
        "description": "Sending data to external servers",
        "patterns": [
            r"curl\s+.*(-d|--data|--data-binary|--data-urlencode|-F|--form)\s+.*@",
            r"curl\s+.*(-X\s+POST|-X\s+PUT)\s+https?://(?!localhost|127\.0\.0\.1)",
            r"wget\s+.*--post-(data|file)",
            r"Invoke-WebRequest\s+.*-Method\s+Post",
            r"Invoke-RestMethod\s+.*-Method\s+Post",
            r"requests\.\s*(post|put)\s*\(",
            r"urllib\.request\.urlopen\s*\(",
            r"fetch\s*\(.+,\s*\{[^}]*method\s*:\s*['\"]POST['\"]",
            r"\.ajax\s*\(",
            r"nslookup\s+.*\$",
            r"dig\s+.*\$",
            r"echo\s+.*\|\s*base64\s*\|\s*(curl|wget|nc|ncat)",
        ],
    },
    # Credential access
    {
        "id": "MS-003",
        "name": "Credential Access",
        "severity": "CRITICAL",
        "description": "Access to credential files or sensitive environment variables",
        "patterns": [
            r"cat\s+.*(/.ssh/|/.aws/|/.gnupg/|/.npmrc|/.netrc|/.docker/config)",
            r"type\s+.*\\(\.ssh|\.aws|\.gnupg|\.npmrc|\.netrc)",
            r"Get-Content\s+.*\\(\.ssh|\.aws|\.gnupg|\.npmrc|\.netrc)",
            r"\$env:(AWS_|GITHUB_|OPENAI_|ANTHROPIC_|API_|SECRET_|TOKEN_|PASSWORD|PRIVATE)",
            r"os\.environ\s*\[\s*['\"]?(AWS_|GITHUB_|OPENAI_|ANTHROPIC_|API_|SECRET_|TOKEN_|PASSWORD|PRIVATE)",
            r"process\.env\s*\.\s*(AWS_|GITHUB_|OPENAI_|ANTHROPIC_|API_|SECRET_|TOKEN_|PASSWORD|PRIVATE)",
            r"printenv\s+(AWS_|GITHUB_|OPENAI_|ANTHROPIC_|API_|SECRET_|TOKEN_)",
            r"cat\s+.*/etc/(passwd|shadow|sudoers)",
            r"cat\s+.*/\.bash_history",
            r"Get-ItemProperty\s+.*\\(Credentials|Passwords|Tokens)",
            r"[Cc]redential[Mm]anager|[Kk]eychain|[Ss]ecret[Ss]tore",
            r"security\s+find-generic-password",
            r"security\s+find-internet-password",
        ],
    },
    # Code obfuscation
    {
        "id": "MS-004",
        "name": "Code Obfuscation",
        "severity": "HIGH",
        "description": "Obfuscated code that hides malicious intent",
        "patterns": [
            r"\beval\s*\(",
            r"\bexec\s*\(",
            r"base64\s*[\.\-]\s*(decode|d\b|--decode|-d)",
            r"atob\s*\(",
            r"btoa\s*\(",
            r"String\.fromCharCode\s*\(",
            r"\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}",
            r"\\u[0-9a-fA-F]{4}\\u[0-9a-fA-F]{4}",
            r"chr\s*\(\s*\d+\s*\)\s*\+\s*chr\s*\(",
            r"compile\s*\(.+\)\s*\.\s*exec",
            r"\[System\.Convert\]::FromBase64String",
            r"\[System\.Text\.Encoding\]::\w+\.GetString",
            r"iex\s*\(",
            r"Invoke-Expression",
            r"-[Ee]ncodedCommand",
            r"-[Ee][Nn][Cc]\s+[A-Za-z0-9+/=]{20,}",
        ],
    },
    # Destructive operations
    {
        "id": "MS-005",
        "name": "Destructive Operations",
        "severity": "HIGH",
        "description": "Operations that can destroy data or damage the system",
        "patterns": [
            r"rm\s+-(rf|fr)\s+(/|~/|\$HOME|\$\{HOME\}|\.\.)",
            r"rm\s+-(rf|fr)\s+\*",
            r"del\s+/[sS]\s+/[qQ]",
            r"Remove-Item\s+.*-Recurse\s+.*-Force",
            r"format\s+[a-zA-Z]:\s*/",
            r"mkfs\.",
            r"dd\s+if=.+of=/dev/",
            r">\s*/dev/sd[a-z]",
            r"shred\s+",
            r"wipe\s+",
            r":()\{.*\|.*&\s*\};:",  # Fork bomb
            r"chmod\s+(-R\s+)?777\s+/",
            r"chown\s+(-R\s+)?\w+:\w+\s+/",
        ],
    },
    # Supply chain attacks
    {
        "id": "MS-006",
        "name": "Supply Chain Attack",
        "severity": "HIGH",
        "description": "Installation of suspicious packages or modification of package configurations",
        "patterns": [
            r"pip\s+install\s+(?!-r\s)(?!--upgrade\s+pip)(?!-e\s+\.).*(?:--index-url|--extra-index-url|-i\s)",
            r"npm\s+install\s+.*--registry\s+",
            r"curl\s+.*\|\s*(bash|sh|python|perl|ruby|node)",
            r"wget\s+.*\|\s*(bash|sh|python|perl|ruby|node)",
            r"Invoke-WebRequest.*\|\s*Invoke-Expression",
            r"iwr\s+.*\|\s*iex",
            r"pip\s+install\s+--pre\s+",
            r"npm\s+install\s+.*@latest\s+--force",
        ],
    },
    # Shell config modification
    {
        "id": "MS-007",
        "name": "Shell Config Modification",
        "severity": "HIGH",
        "description": "Modification of shell or system configurations",
        "patterns": [
            r">>\s*~/?\.(bashrc|zshrc|profile|bash_profile|zprofile|cshrc|tcshrc|config/fish)",
            r"echo\s+.+>>\s*~/?\.",
            r"tee\s+(-a\s+)?~/?\.",
            r"Add-Content\s+.*\\\$PROFILE",
            r"Set-Content\s+.*\\\$PROFILE",
            r"reg\s+add\s+",
            r"New-ItemProperty\s+.*HKLM",
            r"New-ItemProperty\s+.*HKCU",
            r"schtasks\s+/create",
            r"crontab\s+",
            r"systemctl\s+enable\s+",
        ],
    },
    # Crypto mining
    {
        "id": "MS-008",
        "name": "Crypto Mining",
        "severity": "CRITICAL",
        "description": "Attempt to use system resources for cryptocurrency mining",
        "patterns": [
            r"(?i)(xmrig|ccminer|cpuminer|bfgminer|cgminer|ethminer|nbminer|t-rex|phoenixminer|lolminer)",
            r"(?i)stratum\+tcp://",
            r"(?i)stratum\+ssl://",
            r"(?i)(pool|mine)\.(monero|bitcoin|ethereum|crypto|nicehash|2miners|f2pool|nanopool)",
            r"(?i)wallet[\-_]?address",
            r"(?i)mining[\-_]?pool",
            r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}",  # Bitcoin address pattern
            r"4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}",  # Monero address pattern
        ],
    },
]


# ============================================================================
# SCANNER ENGINE
# ============================================================================


class Finding:
    """Represents a single security finding."""

    def __init__(self, rule_id, name, severity, description, file_path,
                 line_number, line_content, matched_text, category):
        self.rule_id = rule_id
        self.name = name
        self.severity = severity
        self.description = description
        self.file_path = file_path
        self.line_number = line_number
        self.line_content = line_content.strip()
        self.matched_text = matched_text
        self.category = category

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "severity": self.severity,
            "description": self.description,
            "category": self.category,
            "file": self.file_path,
            "line": self.line_number,
            "line_content": self.line_content[:200],  # Truncate long lines
            "matched_text": self.matched_text[:100],
        }


def scan_content(content: str, file_path: str, patterns_list: list,
                 category: str) -> list:
    """Scan content against a list of pattern groups."""
    findings = []
    lines = content.split("\n")

    for pattern_group in patterns_list:
        rule_id = pattern_group["id"]
        name = pattern_group["name"]
        severity = pattern_group["severity"]
        description = pattern_group["description"]

        for pattern in pattern_group["patterns"]:
            try:
                regex = re.compile(pattern)
            except re.error:
                continue

            for i, line in enumerate(lines, 1):
                for match in regex.finditer(line):
                    findings.append(Finding(
                        rule_id=rule_id,
                        name=name,
                        severity=severity,
                        description=description,
                        file_path=file_path,
                        line_number=i,
                        line_content=line,
                        matched_text=match.group(0),
                        category=category,
                    ))

    return findings


def check_zero_width_chars(content: str, file_path: str) -> list:
    """Check for zero-width characters that could hide instructions."""
    findings = []
    zero_width = {
        "\u200b": "ZERO WIDTH SPACE",
        "\u200c": "ZERO WIDTH NON-JOINER",
        "\u200d": "ZERO WIDTH JOINER",
        "\ufeff": "BYTE ORDER MARK (BOM)",
        "\u2060": "WORD JOINER",
        "\u2061": "FUNCTION APPLICATION",
        "\u2062": "INVISIBLE TIMES",
        "\u2063": "INVISIBLE SEPARATOR",
        "\u2064": "INVISIBLE PLUS",
        "\u180e": "MONGOLIAN VOWEL SEPARATOR",
        "\u00ad": "SOFT HYPHEN",
    }

    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        for char, name in zero_width.items():
            if char in line:
                # Get surrounding context
                idx = line.index(char)
                context_start = max(0, idx - 20)
                context_end = min(len(line), idx + 20)
                context = line[context_start:context_end]

                findings.append(Finding(
                    rule_id="ZW-001",
                    name="Zero-Width Character",
                    severity="CRITICAL",
                    description=f"Invisible character found: {name} (U+{ord(char):04X}). "
                                f"May hide malicious instructions invisible to the human eye.",
                    file_path=file_path,
                    line_number=i,
                    line_content=f"[hidden char at col {idx}] {context!r}",
                    matched_text=f"U+{ord(char):04X} ({name})",
                    category="HIDDEN_CONTENT",
                ))

    return findings


def check_suspicious_urls(content: str, file_path: str) -> list:
    """Check for suspicious URLs in content."""
    findings = []
    lines = content.split("\n")

    url_pattern = re.compile(
        r"https?://([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})"
    )

    # Known safe domains
    safe_domains = {
        "github.com", "githubusercontent.com", "github.io",
        "gitlab.com", "bitbucket.org",
        "npmjs.com", "npmjs.org",
        "pypi.org", "pypi.python.org",
        "docs.python.org", "python.org",
        "nodejs.org", "deno.land",
        "microsoft.com", "visualstudio.com",
        "stackoverflow.com",
        "mozilla.org", "developer.mozilla.org",
        "google.com", "googleapis.com",
        "aws.amazon.com", "docs.aws.amazon.com",
        "localhost", "127.0.0.1",
        "example.com", "example.org",
    }

    # Suspicious TLDs and patterns
    suspicious_tlds = {".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".work", ".click"}

    for i, line in enumerate(lines, 1):
        for match in url_pattern.finditer(line):
            domain = match.group(1).lower()
            full_url = match.group(0)

            # Skip safe domains
            if any(domain == safe or domain.endswith("." + safe) for safe in safe_domains):
                continue

            severity = "LOW"
            description = f"External URL found: {full_url}"

            # Check for suspicious TLDs
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                severity = "HIGH"
                description = f"URL with suspicious TLD: {full_url}"

            # Check for IP addresses instead of domains
            if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
                severity = "HIGH"
                description = f"URL using direct IP (may bypass DNS filters): {full_url}"

            # Check for typosquatting indicators
            common_typos = {
                "githuh": "github", "gihtub": "github",
                "gogle": "google", "goggle": "google",
                "stackoverfiow": "stackoverflow",
                "mlcrosoft": "microsoft", "micr0soft": "microsoft",
            }
            for typo, real in common_typos.items():
                if typo in domain:
                    severity = "CRITICAL"
                    description = f"Possible typosquatting: '{domain}' looks like '{real}'"

            findings.append(Finding(
                rule_id="URL-001",
                name="External URL",
                severity=severity,
                description=description,
                file_path=file_path,
                line_number=i,
                line_content=line,
                matched_text=full_url,
                category="NETWORK",
            ))

    return findings


def scan_skill(skill_path: str) -> dict:
    """Run the full security scan on a skill directory."""
    skill_path = os.path.abspath(skill_path)
    all_findings = []
    scanned_files = []
    file_stats = {}

    # Collect all files
    for root, dirs, files in os.walk(skill_path):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for fname in files:
            if fname.startswith("."):
                continue

            fpath = os.path.join(root, fname)
            rel_path = os.path.relpath(fpath, skill_path)

            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except (PermissionError, OSError) as e:
                print(f"Warning: Could not read {rel_path}: {e}", file=sys.stderr)
                continue

            scanned_files.append(rel_path)
            file_stats[rel_path] = {
                "lines": len(content.split("\n")),
                "chars": len(content),
                "size_bytes": os.path.getsize(fpath),
            }

            # Determine file type for targeted scanning
            ext = os.path.splitext(fname)[1].lower()
            is_markdown = ext in (".md", ".markdown", ".mdx")
            is_script = ext in (".py", ".js", ".ts", ".sh", ".bash", ".ps1",
                                ".psm1", ".bat", ".cmd", ".rb", ".pl", ".php")
            is_config = ext in (".json", ".yaml", ".yml", ".toml", ".ini", ".cfg")

            # Scan for prompt injection (all files, but especially markdown)
            all_findings.extend(
                scan_content(content, rel_path, PROMPT_INJECTION_PATTERNS,
                             "PROMPT_INJECTION")
            )

            # Scan for malicious script patterns
            all_findings.extend(
                scan_content(content, rel_path, MALICIOUS_SCRIPT_PATTERNS,
                             "MALICIOUS_SCRIPT")
            )

            # Check for zero-width characters
            all_findings.extend(
                check_zero_width_chars(content, rel_path)
            )

            # Check URLs
            all_findings.extend(
                check_suspicious_urls(content, rel_path)
            )

    # Deduplicate findings (same rule, same file, same line)
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f.rule_id, f.file_path, f.line_number, f.matched_text)
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    # Calculate risk level
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in unique_findings:
        severity_counts[f.severity] = severity_counts.get(f.severity, 0) + 1

    if severity_counts["CRITICAL"] > 0:
        risk_level = "CRITICAL"
        risk_emoji = "⚫"
        risk_action = "Do NOT install. Active attack attempt detected."
    elif severity_counts["HIGH"] >= 3:
        risk_level = "HIGH"
        risk_emoji = "🔴"
        risk_action = "Do NOT install. Multiple malicious patterns detected."
    elif severity_counts["HIGH"] > 0:
        risk_level = "MEDIUM"
        risk_emoji = "🟠"
        risk_action = "Review manually before installing."
    elif severity_counts["LOW"] > 0 or severity_counts["MEDIUM"] > 0:
        risk_level = "LOW"
        risk_emoji = "🟡"
        risk_action = "Install with caution. Minor warnings found."
    else:
        risk_level = "SAFE"
        risk_emoji = "🟢"
        risk_action = "No security issues detected by automated scanner."

    return {
        "skill_path": skill_path,
        "risk_level": risk_level,
        "risk_emoji": risk_emoji,
        "risk_action": risk_action,
        "summary": {
            "total_findings": len(unique_findings),
            "severity_counts": severity_counts,
            "files_scanned": len(scanned_files),
            "scanned_files": scanned_files,
        },
        "file_stats": file_stats,
        "findings": [f.to_dict() for f in unique_findings],
    }


# ============================================================================
# OUTPUT FORMATTERS
# ============================================================================


def format_json(result: dict) -> str:
    """Format scan results as JSON."""
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_text(result: dict) -> str:
    """Format scan results as human-readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"  SKILL SECURITY SCAN REPORT")
    lines.append(f"  {result['risk_emoji']} Risk Level: {result['risk_level']}")
    lines.append("=" * 60)
    lines.append(f"\nSkill Path: {result['skill_path']}")
    lines.append(f"Files Scanned: {result['summary']['files_scanned']}")
    lines.append(f"Total Findings: {result['summary']['total_findings']}")
    lines.append(f"\nSeverity Breakdown:")

    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = result["summary"]["severity_counts"].get(sev, 0)
        if count > 0:
            icon = {"CRITICAL": "⚫", "HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}[sev]
            lines.append(f"  {icon} {sev}: {count}")

    lines.append(f"\nRecommendation: {result['risk_action']}")

    if result["findings"]:
        lines.append(f"\n{'─' * 60}")
        lines.append("FINDINGS DETAIL:")
        lines.append(f"{'─' * 60}")

        for f in result["findings"]:
            lines.append(f"\n[{f['severity']}] {f['rule_id']} — {f['name']}")
            lines.append(f"  Category: {f['category']}")
            lines.append(f"  File: {f['file']}:{f['line']}")
            lines.append(f"  Description: {f['description']}")
            lines.append(f"  Match: {f['matched_text']}")
            lines.append(f"  Line: {f['line_content'][:120]}")

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Security scanner for Agent Skills. Checks for prompt injection, "
                    "malicious scripts, data exfiltration, and other threats. "
                    "Supports multilingual detection (EN/PT/ES).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Threat categories scanned:
              PROMPT_INJECTION   Identity override, instruction bypass, permission escalation
              MALICIOUS_SCRIPT   Reverse shells, credential theft, destructive operations
              HIDDEN_CONTENT     Zero-width characters, hidden HTML comments
              NETWORK            Suspicious URLs, typosquatting, data exfiltration

            Languages supported:
              English, Portuguese (PT-BR), Spanish (partial)

            Severity levels:
              CRITICAL   Active attack attempt detected — do not install
              HIGH       Suspicious pattern likely malicious — investigate before use
              MEDIUM     Potentially risky pattern — review carefully
              LOW        Minor concern — note for awareness

            Exit codes:
              0  No findings (SAFE)
              1  Findings detected (check severity)
              2  Invalid arguments or scan error

            Examples:
              %(prog)s --skill-path .agents/skills/downloaded-skill
              %(prog)s --skill-path ./third-party-skill --output json
              %(prog)s --skill-path ./suspicious-skill --output text
        """),
    )
    parser.add_argument(
        "--skill-path",
        required=True,
        help="Path to the skill directory to scan",
    )
    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.skill_path):
        print(
            f"Error: Not a directory: {args.skill_path}\n"
            f"Provide the path to the skill directory to scan.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Check for SKILL.md
    skill_md = os.path.join(args.skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        print(
            f"Warning: No SKILL.md found at {args.skill_path}. "
            f"This may not be a valid skill directory. Scanning anyway...",
            file=sys.stderr,
        )

    print(f"Scanning: {os.path.abspath(args.skill_path)}", file=sys.stderr)

    result = scan_skill(args.skill_path)

    if args.output == "json":
        print(format_json(result))
    else:
        print(format_text(result))

    sys.exit(0 if result["risk_level"] == "SAFE" else 1)


if __name__ == "__main__":
    main()

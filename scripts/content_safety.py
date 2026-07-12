from __future__ import annotations

import re
from pathlib import Path


SECRET_NAMES = {
    ".env", ".env.local", ".env.production", ".npmrc", ".pypirc",
    "id_rsa", "id_ed25519",
}
SECRET_SUFFIXES = {".key", ".p12", ".pem", ".pfx"}
BYTE_PATTERNS = {
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "OpenAI API key": re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "GitHub fine-grained token": re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    "GitLab token": re.compile(rb"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "Slack token": re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "Stripe secret": re.compile(rb"\bsk_(?:live|test)_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    "Google API key": re.compile(rb"\bAIza[0-9A-Za-z_-]{35}\b"),
    "credential in URL": re.compile(rb"https?://[^\s/:]+:[^\s/@]+@"),
}
TEXT_PATTERNS = {
    "Windows user path": re.compile(
        r"(?i)\b[A-Z]:[\\/](?:Users|Documents and Settings)[\\/][^\\/\s]+[\\/]"
    ),
    "Unix user path": re.compile(
        r"(?<!https:)(?<!http:)/(?:Users|home)/[A-Za-z0-9._-]+/"
    ),
    "WSL user path": re.compile(
        r"/mnt/[a-z]/Users/[A-Za-z0-9._-]+/", re.IGNORECASE
    ),
}


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    if path.name.lower() in SECRET_NAMES:
        findings.append("secret-bearing filename")
    if path.suffix.lower() in SECRET_SUFFIXES:
        findings.append("secret-bearing suffix")
    data = path.read_bytes()
    findings.extend(label for label, pattern in BYTE_PATTERNS.items() if pattern.search(data))
    text = data.decode("utf-8", errors="ignore")
    findings.extend(label for label, pattern in TEXT_PATTERNS.items() if pattern.search(text))
    return findings


def require_safe_file(path: Path, label: str) -> None:
    findings = scan_file(path)
    if findings:
        raise ValueError(f"{label}: {', '.join(sorted(set(findings)))}")

#!/usr/bin/env python3
"""Fetch upstream Clash rule set and convert to Loon .list format.

Handles two upstream shapes:
1. Plain .list (what viewer12/OverseasAI.list ships today for both
   Clash and Loon): lines like `DOMAIN,example.com`,
   `DOMAIN-SUFFIX,example.com`, plus `#` comment headers.
   These pass through unchanged.
2. Clash YAML rule-provider: a `payload:` list like
   `  - DOMAIN-SUFFIX,example.com`. The `- ` prefix and the
   `payload:` wrapper are stripped, rule lines are kept.

Usage: python3 scripts/convert.py <upstream_url> <output_path>
"""
import sys
import urllib.request

VALID_PREFIXES = (
    "DOMAIN,", "DOMAIN-SUFFIX,", "DOMAIN-KEYWORD,",
    "DOMAIN-WILDCARD,", "IP-CIDR,", "IP-CIDR6,", "IP-ASN,",
    "GEOIP,", "USER-AGENT,", "URL-REGEX,",
)


def convert(text: str) -> str:
    lines = []
    in_payload = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            lines.append(line)
            continue
        if line == "payload:":
            in_payload = True
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        if line.startswith("payload:"):
            continue
        # Keep only recognised rule lines; drop yaml keys etc.
        if line.startswith(VALID_PREFIXES):
            lines.append(line)
        elif in_payload:
            # Inside a yaml payload, anything else is not a rule.
            continue
        else:
            # Unknown non-comment line in a plain .list: keep it only
            # if it looks like a rule (TYPE,value), otherwise drop.
            continue
    return "\n".join(lines) + "\n"


def main() -> None:
    url, out = sys.argv[1], sys.argv[2]
    with urllib.request.urlopen(url, timeout=30) as r:
        text = r.read().decode("utf-8")
    converted = convert(text)
    with open(out, "w", encoding="utf-8") as f:
        f.write(converted)
    rules = sum(1 for l in converted.splitlines() if not l.startswith("#"))
    print(f"Wrote {out}: {rules} rules")


if __name__ == "__main__":
    main()

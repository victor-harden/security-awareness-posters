#!/usr/bin/env python3
"""Generate security-awareness posters as SVG."""
from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

TOPICS = {
    "passwords": {
        "headline": "One password per account",
        "rules": ["Use a password manager", "Never reuse a password",
                  "Turn on breach alerts"],
        "footer": "Security team - report anything unusual",
    },
    "mfa": {
        "headline": "Turn on MFA today",
        "rules": ["Something you know", "Something you have",
                  "Never share a one-time code"],
        "footer": "MFA blocks most account takeovers",
    },
    "phishing": {
        "headline": "Check before you click",
        "rules": ["Look at the real domain", "Unexpected urgency is a warning",
                  "Report, do not forward"],
        "footer": "Report suspicious messages in one click",
    },
    "updates": {
        "headline": "Updates are security",
        "rules": ["Install updates weekly", "Reboot when asked",
                  "Do not postpone critical patches"],
        "footer": "Most exploited bugs already have a fix",
    },
    "backups": {
        "headline": "Backups beat ransomware",
        "rules": ["Keep one copy offline", "Test a restore every month",
                  "Know your recovery time"],
        "footer": "An untested backup is a hope, not a plan",
    },
    "clean-desk": {
        "headline": "Lock it or lose it",
        "rules": ["Lock your screen when you leave", "No passwords on paper",
                  "Shred sensitive printouts"],
        "footer": "Physical access is still access",
    },
}

THEMES = {
    "light": {"bg": "#ffffff", "fg": "#0f172a", "accent": "#0ea5e9"},
    "dark": {"bg": "#0f172a", "fg": "#e2e8f0", "accent": "#38bdf8"},
}


def build_svg(topic: str, theme: str = "light") -> str:
    if topic not in TOPICS:
        raise KeyError(f"unknown topic: {topic}")
    colors = THEMES.get(theme, THEMES["light"])
    data = TOPICS[topic]
    rules = "".join(
        f'<text x="90" y="{480 + index * 90}" font-size="34" fill="{colors["fg"]}">'
        f'{index + 1}. {html.escape(rule)}</text>'
        for index, rule in enumerate(data["rules"])
    )
    bg, fg, accent = colors["bg"], colors["fg"], colors["accent"]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 794 1123" '
        'width="794" height="1123">',
        f'  <rect width="794" height="1123" fill="{bg}"/>',
        f'  <rect x="0" y="0" width="24" height="1123" fill="{accent}"/>',
        f'  <text x="90" y="150" font-size="26" fill="{accent}" '
        'font-family="sans-serif">SECURITY AWARENESS</text>',
        f'  <text x="90" y="280" font-size="56" font-weight="bold" fill="{fg}" '
        f'font-family="sans-serif">{html.escape(data["headline"])}</text>',
        '  ' + rules,
        f'  <text x="90" y="1020" font-size="24" fill="{accent}" '
        f'font-family="sans-serif">{html.escape(data["footer"])}</text>',
        '</svg>',
        '',
    ]
    return "\n".join(parts)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Security awareness poster generator")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--topic")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--theme", choices=sorted(THEMES), default="light")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args(argv)

    if args.list:
        for name, data in TOPICS.items():
            print(f"{name:<12} {data['headline']}")
        return 0

    if args.all:
        out_dir = args.out_dir or Path("posters")
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in TOPICS:
            (out_dir / f"{name}.svg").write_text(build_svg(name, args.theme),
                                                 encoding="utf-8")
        print(f"wrote {len(TOPICS)} posters to {out_dir}")
        return 0

    if not args.topic or not args.out:
        parser.error("provide --topic and --out (or --list / --all)")
    try:
        svg = build_svg(args.topic, args.theme)
    except KeyError as exc:
        print(exc, file=sys.stderr)
        return 2
    args.out.write_text(svg, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# security-awareness-posters

A small generator for clean, printable security-awareness posters. Each poster is
a standalone SVG (A4 proportions) built from a topic definition: headline, three
rules and a footer. No design tool and no external images required.

## Features

- Topic library covering passwords, MFA, phishing, updates, backups and clean desk.
- `--list`, `--topic`, `--out` and `--all` commands.
- Valid SVG output (checked by tests with an XML parser).
- Text is escaped, so topics can contain `&` or `<` safely.
- Light and dark themes.

## Installation

```bash
git clone https://github.com/victor-harden/security-awareness-posters.git
cd security-awareness-posters
```

## Usage

```bash
python3 poster_gen.py --list
python3 poster_gen.py --topic mfa --out mfa.svg
python3 poster_gen.py --all --out-dir posters
```

Print at A4 or embed in an intranet page.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT — see [LICENSE](LICENSE).

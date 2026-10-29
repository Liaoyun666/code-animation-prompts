"""Copy the complete skill to Claude Code or Codex. No third-party packages."""
import argparse
import shutil
import sys
from pathlib import Path

NAME = "code-animation-prompts"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / NAME


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["codex", "claude", "both"], required=True)
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    base = Path.home() if args.scope == "user" else args.project_dir.resolve()
    targets = ["codex", "claude"] if args.target == "both" else [args.target]
    destinations = [base / (".agents" if t == "codex" else ".claude") / "skills" / NAME for t in targets]
    if not (SOURCE / "SKILL.md").is_file() or not (SOURCE / "references/catalog.json").is_file():
        parser.error("Source skill is incomplete; clone/download the full repository.")
    for dest in destinations:
        if dest.exists() or dest.is_symlink():
            parser.error(f"Destination already exists; preserved without changes: {dest}")
        if SOURCE.resolve() == dest.resolve() or SOURCE.resolve() in dest.resolve().parents:
            parser.error("Destination must be outside the source skill.")
    for target, dest in zip(targets, destinations):
        print(f"{target}: {dest}")
        if not args.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(SOURCE, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print("Dry run: no files changed." if args.dry_run else "Installed. Start a new session to discover the skill.")


if __name__ == "__main__":
    main()

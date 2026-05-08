from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pageindex_adapter import PageIndexAdapter


DATA_DIR = Path(os.environ.get("BANYANTREE_DATA_DIR", PROJECT_ROOT / "data")).resolve()
FINANCIAL_KG_ROOT = Path(os.environ.get("BANYANTREE_FINANCIAL_KG_ROOT", DATA_DIR / "financial_kg")).resolve()
PAGEINDEX_INPUT_DIR = Path(os.environ.get("BANYANTREE_PAGEINDEX_INPUT_DIR", FINANCIAL_KG_ROOT / "pageindex" / "inputs")).resolve()
PAGEINDEX_OUTPUT_DIR = Path(os.environ.get("BANYANTREE_PAGEINDEX_OUTPUT_DIR", FINANCIAL_KG_ROOT / "pageindex" / "outputs")).resolve()
PAGEINDEX_STRUCTURES_DIR = Path(os.environ.get("BANYANTREE_PAGEINDEX_STRUCTURES_DIR", FINANCIAL_KG_ROOT / "pageindex" / "structures")).resolve()
PAGEINDEX_MODEL = os.environ.get("BANYANTREE_PAGEINDEX_MODEL", "gpt-4o-mini")


def _find_pageindex_command() -> list[str] | None:
    command = shutil.which("pageindex")
    if command:
        return [command]

    module_probe = subprocess.run(
        [sys.executable, "-c", "import pageindex"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if module_probe.returncode == 0:
        return [sys.executable, "-m", "pageindex"]

    return None


def _print_manual_instructions(adapter: PageIndexAdapter, docs: list[Path]) -> None:
    print("PageIndex is not installed or does not expose a known CLI entry point.")
    print()
    print("Install optional PageIndex dependencies only when you want to index documents:")
    print("  python -m pip install -r requirements-pageindex.txt")
    print()
    print("Recommended indexing LLM for PageIndex:")
    print(f"  BANYANTREE_PAGEINDEX_MODEL={PAGEINDEX_MODEL}")
    print("  OPENAI_API_KEY=your_api_key  # or any LiteLLM-supported provider key")
    print()
    print(f"Input documents directory: {adapter.input_dir}")
    print(f"Expected structure output directory: {adapter.structures_dir}")
    print()
    if docs:
        print("Documents waiting for PageIndex indexing:")
        for doc in docs:
            print(f"  - {doc}")
    else:
        print("No supported input docs found. Add .pdf, .md, .markdown, or .txt files first.")


def main() -> int:
    adapter = PageIndexAdapter(
        input_dir=PAGEINDEX_INPUT_DIR,
        output_dir=PAGEINDEX_OUTPUT_DIR,
        structures_dir=PAGEINDEX_STRUCTURES_DIR,
    )
    docs = adapter.discover_documents()
    command = _find_pageindex_command()
    if command is None:
        _print_manual_instructions(adapter, docs)
        return 0

    if not docs:
        print(f"No PageIndex input docs found in {adapter.input_dir}")
        return 0

    print(f"Found PageIndex command: {' '.join(command)}")
    print(f"Indexing model: {PAGEINDEX_MODEL}")
    print("This runner is intentionally conservative. If the installed PageIndex CLI")
    print("expects different flags, copy the printed command and adjust it manually.")
    print()

    for doc in docs:
        structure_path = adapter.structure_path_for(doc)
        if structure_path.exists():
            print(f"Skipping already-indexed doc: {doc}")
            continue
        candidate_command = command + [
            "--input",
            str(doc),
            "--output",
            str(structure_path),
            "--model",
            PAGEINDEX_MODEL,
        ]
        print("Suggested command:")
        print("  " + " ".join(candidate_command))
        print("Not executing automatically until PageIndex CLI flags are confirmed for this install.")

    print()
    print("After structures are created, run:")
    print("  python scripts/import_pageindex_docs.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

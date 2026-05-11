#!/usr/bin/env python3
"""Convert all PDF files in a folder to UTF-8 text files.

Example on Windows PowerShell:
    python scripts/pdf_to_txt.py "D:\\大四下\\ISE331\\final_exam"

The script creates an extracted_text folder inside the input folder by default.
"""

from __future__ import annotations

import argparse
from pathlib import Path



def convert_pdf(pdf_path: Path, output_dir: Path) -> Path:
    """Extract text from one PDF and write it to a .txt file."""
    import fitz

    document = fitz.open(pdf_path)
    pages: list[str] = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()
        pages.append(f"\n\n===== {pdf_path.name} | Page {page_number} =====\n\n{text}")

    output_path = output_dir / f"{pdf_path.stem}.txt"
    output_path.write_text("\n".join(pages), encoding="utf-8")
    return output_path


def convert_folder(input_dir: Path, output_dir: Path) -> list[Path]:
    """Convert every PDF directly inside input_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_paths = sorted(input_dir.glob("*.pdf"))

    if not pdf_paths:
        raise FileNotFoundError(f"No PDF files found in: {input_dir}")

    output_paths: list[Path] = []
    for pdf_path in pdf_paths:
        print(f"Reading: {pdf_path.name}")
        output_path = convert_pdf(pdf_path, output_dir)
        output_paths.append(output_path)
        print(f"Saved: {output_path}")

    return output_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text from all PDF files in a folder."
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        default=".",
        help="Folder containing PDF files. Default: current folder.",
    )
    parser.add_argument(
        "--output-dir",
        help="Folder for generated .txt files. Default: <input_dir>/extracted_text.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir).expanduser().resolve()
    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else input_dir / "extracted_text"
    )

    print(f"Input folder: {input_dir}")
    print(f"Output folder: {output_dir}")
    output_paths = convert_folder(input_dir, output_dir)
    print(f"Done. Converted {len(output_paths)} PDF file(s).")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Optional

import music21


def _svg_to_markdown_data_uri(svg_content: str) -> str:
    svg_b64 = base64.b64encode(svg_content.encode("utf-8")).decode("ascii")
    return f"![score](data:image/svg+xml;base64,{svg_b64})"


def _find_verovio_candidate() -> Optional[str]:
    return shutil.which("verovio")


def _call_verovio_export(verovio_path: str, in_path: str, out_path: str) -> None:
    cmd = [verovio_path, "-o", out_path, in_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Verovio export failed: {e}") from e


def musicxml_to_svg(musicxml_path: str, svg_path: str, verovio_path: Optional[str] = None) -> None:
    if not os.path.exists(musicxml_path):
        raise FileNotFoundError(f"Input MusicXML not found: {musicxml_path}")

    try:
        music21.converter.parse(musicxml_path)
    except Exception as e:
        raise RuntimeError(f"music21 failed to parse MusicXML: {e}") from e

    vr = verovio_path or _find_verovio_candidate()
    if not vr:
        raise RuntimeError("Verovio CLI not found on PATH. Install verovio.")

    _call_verovio_export(vr, musicxml_path, svg_path)


def musicxml_string_to_svg(xml_string: str, svg_path: str, verovio_path: Optional[str] = None) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".musicxml", delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(xml_string)
    try:
        musicxml_to_svg(tmp_path, svg_path, verovio_path=verovio_path)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def musicxml_to_svg_string(musicxml_path: str, verovio_path: Optional[str] = None) -> str:
    with tempfile.NamedTemporaryFile("r", suffix=".svg", delete=False) as tmp_svg:
        svg_path = tmp_svg.name
    try:
        musicxml_to_svg(musicxml_path, svg_path, verovio_path=verovio_path)
        with open(svg_path, "r", encoding="utf-8") as f:
            return f.read()
    finally:
        try:
            os.remove(svg_path)
        except OSError:
            pass


def musicxml_string_to_svg_string(xml_string: str, verovio_path: Optional[str] = None) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".musicxml", delete=False) as tmp_xml:
        xml_path = tmp_xml.name
        tmp_xml.write(xml_string)
    try:
        return musicxml_to_svg_string(xml_path, verovio_path=verovio_path)
    finally:
        try:
            os.remove(xml_path)
        except OSError:
            pass


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Convert MusicXML to SVG using Verovio CLI")
    parser.add_argument("musicxml_path", help="Input MusicXML file")
    args = parser.parse_args(argv)

    svg = musicxml_to_svg_string(args.musicxml_path)
    sys.stdout.write(_svg_to_markdown_data_uri(svg))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

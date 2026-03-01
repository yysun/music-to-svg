import shutil
import base64
from pathlib import Path
import pytest
import convert

SIMPLE_MUSICXML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC
  "-//Recordare//DTD MusicXML 3.1 Partwise//EN"
  "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="3.1">
  <part-list>
    <score-part id="P1"><part-name>Music</part-name></score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>1</divisions>
        <key><fifths>0</fifths></key>
        <time><beats>4</beats><beat-type>4</beat-type></time>
        <clef><sign>G</sign><line>2</line></clef>
      </attributes>
      <note>
        <pitch><step>C</step><octave>4</octave></pitch>
        <duration>4</duration>
        <type>whole</type>
      </note>
    </measure>
  </part>
</score-partwise>
"""


def has_musescore_or_verovio() -> bool:
    candidates = ["verovio"]
    return any(shutil.which(c) for c in candidates)


def _echo_markdown(capsys, markdown_text: str) -> None:
  # Temporarily disable capture so markdown is visible in pytest output.
  with capsys.disabled():
    print(markdown_text)

@pytest.mark.skipif(not has_musescore_or_verovio(), reason="No backend (Verovio) available in PATH")
def test_musicxml_string_to_svg():
    out_svg = Path("./out.svg")
    if out_svg.exists():
        out_svg.unlink()

    convert.musicxml_string_to_svg(SIMPLE_MUSICXML, str(out_svg))
    assert out_svg.exists()
    assert out_svg.stat().st_size > 0


def test_main_file_to_stdout(monkeypatch, capsys, tmp_path):
    score = tmp_path / "score.musicxml"
    score.write_text("<score-partwise/>", encoding="utf-8")

    def fake_convert(path, verovio_path=None):
        assert path == str(score)
    assert verovio_path is None
        return "<svg>ok</svg>"

    monkeypatch.setattr(convert, "musicxml_to_svg_string", fake_convert)

    exit_code = convert.main([str(score)])
    captured = capsys.readouterr()
    _echo_markdown(capsys, captured.out)

    assert exit_code == 0
    expected = base64.b64encode("<svg>ok</svg>".encode("utf-8")).decode("ascii")
    assert captured.out == f"![score](data:image/svg+xml;base64,{expected})"

---
name: music-to-svg
description: 'Use the project converter script to render MusicXML to SVG markdown image output. Write MusicXML to a temp file, then pass --file.'
argument-hint: 'MusicXML string'
---

Use only these rules:

1. Use the `write_file` tool to save the MusicXML content to a file (e.g. `/tmp/score.musicxml`).

2. Run script `scripts/convert.py --file /tmp/score.musicxml`

3. Do not invoke renderer CLI commands directly.

4. Output is always stdout markdown image:
`![score](data:image/svg+xml;base64,...)`

5. Render the image as markdown with the base64-encoded SVG data URI. Do not return raw SVG or a file path.
#!/usr/bin/env python3
"""
build_booklet.py  —  Campus IT Service Desk Handover Lab
Builds lab-book/campus-it-handover-lab.pdf from the markdown source.

Conversion strategy (tries in order):
  1. pandoc   — best output; install with  apt-get install -y pandoc
  2. weasyprint + markdown  — pip install markdown weasyprint
  3. HTML output only  — no extra dependencies; open in browser to print/save

Run from the repository root:
    python3 build_booklet.py

The source file must be:
    lab-book/campus-it-handover-lab.md

The output file will be:
    lab-book/campus-it-handover-lab.pdf   (or .html if PDF build fails)
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT   = Path(__file__).resolve().parent
SRC_MD = ROOT / 'lab-book' / 'campus-it-handover-lab.md'
PDF    = ROOT / 'lab-book' / 'campus-it-handover-lab.pdf'
HTML   = ROOT / 'lab-book' / 'campus-it-handover-lab.html'
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

* { box-sizing: border-box; }

body {
    font-family: 'Inter', 'Helvetica Neue', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color:
    max-width: 700px;
    margin: 0 auto;
    padding: 20px 30px;
}

h1 {
    font-size: 20pt;
    font-weight: 700;
    color:
    border-bottom: 3px solid
    padding-bottom: 8px;
    margin-top: 0;
}

h2 {
    font-size: 14pt;
    font-weight: 700;
    color:
    border-left: 4px solid
    padding-left: 10px;
    margin-top: 30px;
}

h3 {
    font-size: 11pt;
    font-weight: 600;
    color:
    margin-top: 18px;
}

code {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 9.5pt;
    background:
    border: 1px solid
    border-radius: 3px;
    padding: 1px 4px;
}

pre {
    background:
    color:
    border-left: 4px solid
    border-radius: 4px;
    padding: 12px 16px;
    overflow-x: auto;
    margin: 10px 0;
}

pre code {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 9pt;
    background: none;
    border: none;
    color:
    padding: 0;
}

blockquote {
    background:
    border-left: 4px solid
    margin: 12px 0;
    padding: 8px 14px;
    border-radius: 0 4px 4px 0;
    color:
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
    font-size: 10pt;
}

th {
    background:
    color:
    padding: 6px 10px;
    text-align: left;
    font-weight: 600;
}

td {
    border: 1px solid
    padding: 5px 10px;
}

tr:nth-child(even) td {
    background:
}

hr {
    border: none;
    border-top: 2px solid
    margin: 24px 0;
}

@media print {
    h2 { page-break-before: auto; }
    pre, table, blockquote { page-break-inside: avoid; }
}
"""

def build_html(md_text):
    """Convert markdown text to a full HTML document string."""
    try:
        import markdown
        body = markdown.markdown(
            md_text,
            extensions=['tables', 'fenced_code', 'codehilite'],
        )
    except ImportError:
        body = f'<pre style="white-space:pre-wrap">{md_text}</pre>'
        print('  (markdown package not found — HTML output is plain text)')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Campus IT Service Desk Handover Lab</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""

def try_pandoc():
    """Try to build PDF with pandoc. Returns True on success."""
    if not shutil.which('pandoc'):
        return False
    try:
        subprocess.run(
            [
                'pandoc', str(SRC_MD),
                '--output', str(PDF),
                '--pdf-engine=weasyprint',
                '--standalone',
                '--metadata', 'title=Campus IT Service Desk Handover Lab',
                '--css', str(ROOT / 'lab-book' / '_style.css'),
                '--variable', 'geometry:margin=20mm',
            ],
            check=True, capture_output=True, text=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    try:
        subprocess.run(
            [
                'pandoc', str(SRC_MD),
                '--output', str(PDF),
                '--pdf-engine=xelatex',
                '--standalone',
                '--variable', 'geometry:margin=20mm',
                '--variable', 'fontsize=11pt',
                '--variable', 'mainfont=DejaVu Sans',
                '--variable', 'monofont=DejaVu Sans Mono',
            ],
            check=True, capture_output=True, text=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    try:
        subprocess.run(
            ['pandoc', str(SRC_MD), '--output', str(PDF), '--standalone'],
            check=True, capture_output=True, text=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def try_weasyprint(html_text):
    """Try to build PDF with weasyprint. Returns True on success."""
    try:
        from weasyprint import HTML as WP_HTML
        WP_HTML(string=html_text, base_url=str(ROOT)).write_pdf(str(PDF))
        return True
    except ImportError:
        return False
    except Exception as exc:
        print(f'  weasyprint failed: {exc}')
        return False

def main():
    if not SRC_MD.exists():
        sys.exit(f'Source not found: {SRC_MD}\nRun from the repository root.')

    md_text = SRC_MD.read_text(encoding='utf-8')
    html_text = build_html(md_text)

    (ROOT / 'lab-book' / '_style.css').write_text(CSS, encoding='utf-8')

    print('Building lab-book/campus-it-handover-lab.pdf ...')
    print()

    if try_pandoc():
        print(f'  PDF built with pandoc:     {PDF}')
        return

    print('  pandoc not found or failed — trying weasyprint ...')
    if try_weasyprint(html_text):
        print(f'  PDF built with weasyprint: {PDF}')
        return

    print('  weasyprint not found or failed — writing HTML ...')
    HTML.write_text(html_text, encoding='utf-8')
    print(f'  HTML written: {HTML}')
    print()
    print('To produce a PDF from the HTML:')
    print('  - Open the HTML file in Chrome or Firefox')
    print('  - File > Print > Save as PDF')
    print('  - Or install pandoc:  sudo apt-get install -y pandoc')
    print()
    print('To install weasyprint:')
    print('  pip install markdown weasyprint')

if __name__ == '__main__':
    main()

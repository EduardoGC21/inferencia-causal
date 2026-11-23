"""Traslada el Markdown aprobado al estilo LaTeX existente, sin recalcular datos."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("markdown", type=Path)
parser.add_argument("tex", type=Path)
parser.add_argument("build", type=Path)
args = parser.parse_args()
source = args.markdown.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
lines = source.splitlines()
args.build.mkdir(parents=True, exist_ok=True)
blocks, ignored, out = [], [], []
title = next(x[2:] for x in lines if x.startswith("# "))
subtitle = next(x[1:-1] for x in lines if x.startswith("*") and not x.startswith("**"))
author = next(x.strip("*") for x in lines if x.startswith("**Eduardo"))
professor = next(x.strip("*") for x in lines if x.startswith("**Profesor:"))
date = next(x for x in lines if x.startswith("Inferencia Causal ·"))

def plain(text):
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
                    "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
                    "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
                    "\u2006": r"\,", "\u2009": r"\,", "\u202f": r"\,",
                    "\u00a0": "~", "–": "--", "—": "---",
                    "«": r"\guillemotleft{}", "»": r"\guillemotright{}",
                    "·": r"\textperiodcentered{}"}
    return "".join(replacements.get(ch, ch) for ch in text)

def inline(text):
    protected = []
    def keep(value):
        protected.append(value)
        return f"\x01{len(protected)-1}\x02"
    text = re.sub(r"\$([^$]+)\$", lambda m: keep("$"+m[1]+"$"), text)
    code_pattern = chr(96)+r"([^"+chr(96)+r"]+)"+chr(96)
    text = re.sub(code_pattern, lambda m: keep(r"\path{"+m[1]+"}"), text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: keep(r"\href{\detokenize{"+m[2]+"}}{"+inline(m[1])+"}"), text)
    text = re.sub(r"<(https?://[^>]+)>", lambda m: keep(r"\url{"+m[1]+"}"), text)
    text = plain(text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: r"\textbf{"+m[1]+"}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: r"\emph{"+m[1]+"}", text)
    for i, value in enumerate(protected):
        text = text.replace(f"\x01{i}\x02", value)
    return text

def cell(text, expanded):
    result = []
    for piece in text.split("<br>"):
        if expanded and piece.startswith("[") and len(piece) > 21 and "; " in piece:
            lower, upper = piece.split("; ", 1)
            result += [inline(lower+";"), inline(upper)]
        else:
            result.append(inline(piece))
    return r"\newline ".join(result)

widths = {
    1: [.26, .26, .19, .145, .145],
    2: [.17, .15, .20, .24, .12, .12],
    3: [.235, .19125, .19125, .19125, .19125],
    4: [.24, .38, .38],
    5: [.14, .14, .25, .08, .39],
    6: [.25, .25, .10, .40],
    7: [.62, .19, .19],
    8: [.19, .14, .07, .11, .245, .245],
    9: [.37, .21, .21, .21],
    10: [.23, .11, .07, .197, .197, .196],
    11: [.12, .13, .285, .09, .285, .09],
    12: [.24, .10, .06, .07, .265, .265],
    13: [.39, .14, .09, .10, .14, .14],
    14: [.22, .10, .23, .23, .22],
    15: [.12, .12, .2533, .2533, .2534],
    16: [.12, .12, .20, .34, .07, .15],
    17: [.11, .10, .15, .09, .12, .09, .13, .21],
    18: [.38, .31, .31],
}
layout_keys = {'1': 1, 'B1': 2, '2': 3, 'G1': 4, 'A1': 5, 'A2': 6, 'A3': 7, 'A4': 8, 'A5': 9, 'B2': 10, 'B3': 11, 'C1': 12, 'C2': 13, 'C3': 14, 'C4': 15, 'D1': 16, 'D2': 17, 'D3': 18}

def table(raw, number, line):
    parsed = [[v.strip() for v in row.strip().strip("|").split("|")] for row in raw]
    header, rows = parsed[0], parsed[2:]
    n = len(header)
    if any(len(row) != n for row in rows):
        raise ValueError(f"Columnas distintas en el cuadro {number}")
    fractions = widths[layout_keys[number]]
    if len(fractions) != n:
        raise ValueError(f"Anchos incorrectos: cuadro {number}")
    available = 6.66*72.27 - 6*(n-1)
    columns = ["@{}"]
    for i, fraction in enumerate(fractions):
        align = r"\RaggedRight" if i == 0 else r"\centering"
        columns.append(">{"+align+r"\arraybackslash}p{"+f"{available*fraction:.3f}"+"pt}")
    columns.append("@{}")
    font, leading = ("9", "11") if n <= 6 else ("8", "9.6")
    header_tex = " & ".join(r"\textbf{"+inline(x)+"}" for x in header)+r" \\"
    rendered = [r"\begingroup\centering",r"\fontsize{"+font+"}{"+leading+r"}\selectfont",
                r"\begin{tabular}{"+ "".join(columns)+"}",r"\toprule",header_tex,r"\midrule"]
    for row in rows:
        rendered.append(" & ".join(cell(x, number == "2") for x in row)+r" \\")
    rendered += [r"\bottomrule",r"\end{tabular}\par",r"\endgroup"]
    blocks.append({"type":"table","line":line,"number":number,
                   "columns":n,"rows":len(rows),"source":raw})
    return "\n".join(rendered)

preamble = r"""\documentclass[11pt,letterpaper]{article}
\usepackage[spanish,es-nodecimaldot,es-noquoting]{babel}
\usepackage[T1]{fontenc}
\usepackage{lmodern,microtype,amsmath,amssymb,graphicx,booktabs}
\microtypesetup{expansion=false}
\usepackage[margin=0.92in]{geometry}
\usepackage{ragged2e,xurl,csquotes}
\usepackage[backend=biber,style=apa,natbib=true,sortcites=true]{biblatex}
\DeclareLanguageMapping{spanish}{spanish-apa}
\addbibresource{referencias.bib}
\setlength{\bibitemsep}{0.1em}
\usepackage{array,longtable,needspace}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdftitle={Narcoataques y siniestros viales registrados},pdfauthor={Eduardo Garcia Cortez},pdfsubject={Inferencia Causal, ITAM; profesor Mauricio Romero}}
\urlstyle{same}
\setlength{\RaggedRightRightskip}{0pt plus 1fil}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.22em}
\setlength{\emergencystretch}{2em}
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\linespread{1.0}
\input{glyphtounicode}
\pdfgentounicode=1
\renewenvironment{abstract}{\par\begin{center}\small\bfseries Resumen\end{center}\small\RaggedRight\noindent}{\par}
"""
out.append(preamble)
out.append(r"\title{\textbf{"+inline(title)+r"}\\[0.2em]\large "+inline(subtitle)+"}")
out.append(r"\author{\normalsize "+inline(author.split(" · ")[0])+r" \quad "+inline(author.split(" · ")[1])+
           r"\\\normalsize "+inline(professor)+"}")
out.append(r"\date{\normalsize "+inline(date)+"}")
out.append(r"\begin{document}\RaggedRight\setlength{\parindent}{0pt}\maketitle")
abstract, references, number, i, table_box = False, False, None, 0, False
if lines[0] == "---":
    end = lines.index("---", 1)
    ignored += list(range(1, end+2))
    i = end+1
while i < len(lines):
    s = lines[i].strip()
    line = i+1
    if not s:
        i += 1
        continue
    if s.startswith("# ") or s == "*"+subtitle+"*" or s in ("**"+author+"**", "**"+professor+"**", date):
        ignored.append(line)
        i += 1
        continue
    if s.startswith("> "):
        ignored.append(line)
        i += 1
        continue
    if s == "## Resumen":
        out.append(r"\begin{abstract}")
        abstract = True
        blocks.append({"type":"heading","line":line,"source":s})
        i += 1
        continue
    if s.startswith("## "):
        if abstract:
            out.append(r"\end{abstract}")
            abstract = False
        if references:
            out.append(r"\endgroup")
            references = False
        heading = s[3:]
        if heading == "Referencias" or (heading.startswith("Apéndice ") and not heading.startswith("Apéndice D.")):
            out.append(r"\clearpage")
        if heading.startswith("2. "):
            out.append(r"\Needspace{8\baselineskip}")
        out.append(r"\section*{"+inline(heading)+"}")
        if heading == "Referencias":
            references = True
            out.append(r"\begingroup\setlength{\parskip}{0.3em}")
        blocks.append({"type":"heading","line":line,"source":s})
        i += 1
        continue
    if s.startswith("### "):
        heading = s[4:]
        command = r"\subsection*" if heading.startswith("3.1.") or heading == "Sensibilidad a la base de comparación" else r"\paragraph"
        out.append(command+"{"+inline(heading)+"}")
        blocks.append({"type":"heading","line":line,"source":s})
        i += 1
        continue
    if s == "$$":
        end = lines.index("$$",i+1)
        math = "\n".join(lines[i+1:end])
        out.append("\\[\n"+math+"\n\\]")
        blocks.append({"type":"display_math","line":line,"source":math})
        i = end+1
        continue
    if s.startswith("**Cuadro "):
        number = re.match(r"\*\*Cuadro ([A-Z]?\d+)", s)[1]
        out += [r"\par\medskip\noindent\begin{minipage}{\linewidth}",
                r"\begin{center}\small "+inline(s)+r"\end{center}"]
        table_box = True
        blocks.append({"type":"table_caption","line":line,"source":s,"number":number})
        i += 1
        continue
    if s.startswith("**Panel "):
        if s.startswith("**Panel B del cuadro 2."):
            number = "2"
        if not table_box:
            out.append(r"\par\medskip\noindent\begin{minipage}{\linewidth}")
            table_box = True
        out.append(inline(s)+r"\par\medskip")
        blocks.append({"type":"panel","line":line,"source":s})
        i += 1
        continue
    if s.startswith("|"):
        raw = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            raw.append(lines[i].strip())
            i += 1
        if not table_box:
            raise ValueError("Cuadro sin título")
        out.append(table(raw, number, line))
        if number not in ("G1", "1"):
            out.append(r"\end{minipage}\par\medskip")
            table_box = False
        continue
    if s.startswith("**Figura "):
        end = i+1
        while end < len(lines) and not lines[end].strip():
            end += 1
        image_line = lines[end].strip()
        match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)",image_line)
        if not match:
            raise ValueError(f"Figura sin imagen adyacente en la línea {line}")
        image = (args.markdown.parent / match[2]).resolve()
        if not image.exists():
            raise FileNotFoundError(image)
        relative_image = Path("figuras") / image.name
        for target_root in (args.tex.parent, args.build):
            target = target_root / relative_image
            target.parent.mkdir(exist_ok=True)
            if not target.exists() or target.read_bytes() != image.read_bytes():
                shutil.copyfile(image, target)
        max_height = r".59\textheight" if "Figura 2." in s else r".66\textheight"
        out += [r"\par\medskip\noindent\begin{minipage}{\linewidth}",r"\begin{center}\small",
                inline(s)+r"\par\medskip",
                r"\includegraphics[width=\linewidth,height="+max_height+r",keepaspectratio]{\detokenize{"+
                relative_image.as_posix()+"}}",r"\end{center}",r"\end{minipage}\par\medskip"]
        blocks.append({"type":"figure","line":line,"source":s,"image_source":image_line,"path":str(image)})
        i = end+1
        continue
    if s.startswith("!["):
        raise ValueError(f"Imagen no procesada en la línea {line}")
    paragraph, end = [s], i+1
    while end < len(lines) and lines[end].strip() and not lines[end].strip().startswith(("#","|","$$","**Cuadro ","**Figura ","**Panel ")):
        paragraph.append(lines[end].strip())
        end += 1
    text = " ".join(paragraph)
    if references:
        out.append(r"\par\hangindent=0.5in\hangafter=1\noindent "+inline(text)+r"\par")
    else:
        following=end
        while following<len(lines) and not lines[following].strip():
            following+=1
        if following<len(lines) and lines[following].strip()=="$":
            out.append(r"\Needspace{8\baselineskip}")
        is_table_note=text.startswith(("Cada celda de coeficientes presenta", "Emparejamiento 1:muchos:", "El $R^2$ ponderado incluye", "Cada celda presenta", "Registros por municipio y día; IC"))
        if is_table_note:
            out.append(r"{\fontsize{9}{11}\selectfont "+inline(text)+r"\par}")
        else:
            if table_box and number == "1":
                out.append(r"\RaggedRight "+inline(text)+r"\par")
            else:
                out.append(inline(text)+r"\par")
    if table_box and ((number == "G1" and text.startswith("Registros por municipio y día; IC")) or
                      (number == "1" and text.startswith("Desviación estándar (DE) ponderada"))):
        out.append(r"\end{minipage}\par\medskip")
        table_box = False
    blocks.append({"type":"reference" if references else "paragraph","line":line,"source":text})
    i = end
if abstract:
    out.append(r"\end{abstract}")
if references:
    out.append(r"\endgroup")
out.append(r"\end{document}")
args.tex.write_text("\n\n".join(out)+"\n",encoding="utf-8")
shutil.copyfile(args.tex.parent/"referencias.bib",args.build/"referencias.bib")
manifest = {"markdown":str(args.markdown),"sha256":hashlib.sha256(args.markdown.read_bytes()).hexdigest(),
            "tex":str(args.tex),"blocks":blocks,"excluded_metadata_lines":ignored,
            "title":title,"subtitle":subtitle,"author":author,"professor":professor,"date":date}
(args.build / "contenido-markdown.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"blocks":len(blocks),"types":{kind:sum(b["type"]==kind for b in blocks) for kind in sorted({b["type"] for b in blocks})},
                  "tex":str(args.tex),"build":str(args.build)},ensure_ascii=False))

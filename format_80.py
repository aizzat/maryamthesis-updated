import textwrap
import re

def format_latex(filepath, width=80):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by blank lines to get paragraphs
    paragraphs = re.split(r'\n[ \t]*\n', content)
    
    skip_prefixes = (
        '\\begin', '\\end', '\\chapter', '\\section', '\\subsection', '\\subsubsection',
        '\\item', '%', '\\label', '\\caption', '\\centering', '\\includegraphics',
        '\\hline', '\\rowcolor', '\\multicolumn', '\\toprule', '\\midrule', '\\bottomrule',
        '\\vspace', '\\hspace', '\\pagebreak', '\\clearpage', '\\noindent', '\\['
    )
    
    out_paragraphs = []
    for p in paragraphs:
        lines = p.split('\n')
        # Check if the paragraph contains any LaTeX commands that shouldn't be wrapped
        if any(line.strip().startswith(skip_prefixes) or '&' in line or '\\\\' in line for line in lines):
            out_paragraphs.append(p)
        else:
            # Join the paragraph into a single line, then wrap
            joined = ' '.join(line.strip() for line in lines if line.strip())
            if joined:
                wrapped = textwrap.fill(joined, width=width)
                out_paragraphs.append(wrapped)
            else:
                out_paragraphs.append(p)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(out_paragraphs) + '\n')

format_latex('Chap1/chap1.tex', 80)
print("Formatted Chap1/chap1.tex to 80 characters!")

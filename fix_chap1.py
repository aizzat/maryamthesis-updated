import re
import textwrap

filepath = 'Chap1/chap1.tex'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix unescaped ampersands
content = re.sub(r'(?<!\\)&', r'\&', content)

# Split into paragraphs
paragraphs = re.split(r'\n[ \t]*\n', content)

skip_prefixes = (
    '\\begin', '\\end', '\\chapter', '\\section', '\\subsection', '\\subsubsection',
    '%', '\\label', '\\caption', '\\centering', '\\includegraphics',
    '\\hline', '\\rowcolor', '\\multicolumn', '\\toprule', '\\midrule', '\\bottomrule',
    '\\vspace', '\\hspace', '\\pagebreak', '\\clearpage', '\\noindent', '\\['
)

out_paragraphs = []
for p in paragraphs:
    lines = p.split('\n')
    # If it contains an equation or specific block, skip wrapping
    if any(line.strip().startswith(skip_prefixes) or '\\\\' in line for line in lines):
        out_paragraphs.append(p)
    else:
        # Wrap the paragraph
        # First, remove extra spaces and newlines
        joined = ' '.join(line.strip() for line in lines if line.strip())
        if joined:
            # Check if it starts with \item
            if joined.startswith('\\item'):
                item_text = joined[5:].strip()
                wrapped = textwrap.fill(item_text, width=74)
                # re-add \item with proper indentation
                wrapped = '\\item ' + wrapped.replace('\n', '\n    ')
                out_paragraphs.append(wrapped)
            else:
                wrapped = textwrap.fill(joined, width=80)
                out_paragraphs.append(wrapped)
        else:
            out_paragraphs.append(p)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(out_paragraphs) + '\n')

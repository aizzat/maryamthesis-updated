import re
import textwrap
import os

def format_latex_file(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
        
    print(f"Formatting {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out_lines = []
    
    skip_prefixes = (
        '\\begin', '\\end', '\\chapter', '\\section', '\\subsection', '\\subsubsection',
        '\\item', '%', '\\label', '\\caption', '\\centering', '\\includegraphics',
        '\\hline', '\\rowcolor', '\\multicolumn', '\\toprule', '\\midrule', '\\bottomrule',
        '\\vspace', '\\hspace', '\\pagebreak', '\\clearpage', '\\noindent', '\\['
    )
    
    for line in lines:
        stripped = line.strip()
        
        if (len(stripped) < 100 or 
            stripped.startswith(skip_prefixes) or 
            '&' in stripped or 
            '\\\\' in stripped):
            out_lines.append(line)
        else:
            # Wrap the long text paragraph
            wrapped = textwrap.fill(line, width=100, break_long_words=False, break_on_hyphens=False, replace_whitespace=True, drop_whitespace=True)
            out_lines.append(wrapped + '\n')
                
    with open(filepath, 'w', encoding='utf-8') as f:
        for l in out_lines:
            f.write(l)

for i in range(1, 6):
    filepath = f"Chap{i}/chap{i}.tex"
    format_latex_file(filepath)


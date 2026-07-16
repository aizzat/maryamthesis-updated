import re
import textwrap

def format_latex_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    out_lines = []
    
    # We will only wrap lines that are very long and seem to be text paragraphs.
    for line in lines:
        stripped = line.strip()
        # If the line is short, or it's a structural command, leave it alone.
        if len(stripped) < 100 or stripped.startswith('\\begin') or stripped.startswith('\\end') or stripped.startswith('\\chapter') or stripped.startswith('\\section') or stripped.startswith('\\subsection') or stripped.startswith('%'):
            out_lines.append(line)
        else:
            # It's a long line. Let's check if it's an item or just text.
            match = re.match(r'^(\s*(?:\\item\s*)?)(.*)$', line)
            if match:
                prefix = match.group(1)
                content = match.group(2)
                
                # We want subsequent wrapped lines to just align with the text part, or just normal indent
                # But LaTeX doesn't care about indent. Let's just wrap it.
                wrapped = textwrap.fill(line, width=100, replace_whitespace=True, drop_whitespace=True)
                out_lines.append(wrapped + '\n')
            else:
                out_lines.append(line)
                
    with open(filepath, 'w') as f:
        for l in out_lines:
            f.write(l)

format_latex_file('Chap1/chap1.tex')

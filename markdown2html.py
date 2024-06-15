#!/usr/bin/env python3

"""
markdown2html.py: A script to convert a Markdown file to an HTML file,
with specific handling for headings, unordered lists, ordered lists,
paragraphs, and bold text.
"""

import sys
import os
import re
import markdown


def convert_markdown_to_html(markdown_text):
    """
    Converts a given Markdown text to HTML,
    with specific handling for headings,
    unordered lists, ordered lists, paragraphs, and bold text.
    """
    lines = markdown_text.splitlines()
    html_lines = []
    in_ulist = False
    in_olist = False
    in_paragraph = False

    def convert_bold_syntax(text):
        """
        Converts Markdown bold syntax to HTML <strong> tags.
        """
        bold_pattern = re.compile(r'(\*\*|__)(.*?)\1')
        return bold_pattern.sub(r'<strong>\2</strong>', text)

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            continue
        if line.startswith('#'):
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            level = len(line.split(' ')[0])
            content = ' '.join(line.split(' ')[1:])
            html_line = f"<h{level}>{convert_bold_syntax(content)}</h{level}>"
            html_lines.append(html_line)
        elif line.startswith(('*', '-', '+')):
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if in_olist:
                html_lines.append("</ol>")
                in_olist = False
            if not in_ulist:
                html_lines.append("<ul>")
                in_ulist = True
            content = line[1:].strip()
            html_line = f"<li>{convert_bold_syntax(content)}</li>"
            html_lines.append(html_line)
        elif stripped_line[0].isdigit() and stripped_line[1] == '.':
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if in_ulist:
                html_lines.append("</ul>")
                in_ulist = False
            if not in_olist:
                html_lines.append("<ol>")
                in_olist = True
            content = line[line.index('.') + 1:].strip()
            html_line = f"<li>{convert_bold_syntax(content)}</li>"
            html_lines.append(html_line)
        else:
            if in_ulist:
                html_lines.append("</ul>")
                in_ulist = False
            if in_olist:
                html_lines.append("</ol>")
                in_olist = False
            if not in_paragraph:
                html_lines.append("<p>")
                in_paragraph = True
            html_line = convert_bold_syntax(line)
            html_lines.append(html_line)

    if in_paragraph:
        html_lines.append("</p>")
    if in_ulist:
        html_lines.append("</ul>")
    if in_olist:
        html_lines.append("</ol>")

    return "\n".join(html_lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r') as md_file:
        md_content = md_file.read()

    html_content = convert_markdown_to_html(md_content)

    with open(html_file, 'w') as html_file:
        html_file.write(html_content)

    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/python3
""" Takes as argument 2 strings, the name of Markdown file
    and the output file name respectively.
    Requirements:
        - if the number of args < 2 print to STDERR
        'Usage: ./markdown2html.py README.md README.html' and exit 1
        - if the Markdown file doesn't exist print in STDERR
        'Missing <filename>' and exit 1
        - otherwise, print nothing and exit 0
"""
import sys
import os


if __name__ == '__main__':
    # define a helper function, isParagraph
    def isParagraph(line, h_level, ol, ul):
        """ checks if a line is a potential paragraph: i.e.
            if h_level == -1 and both ol and ul are false
        """
        if line not in ['\n', '\r', '\r\n']:
            return (h_level == -1 and not ol and not ul)
        return False  # line's a blank line

    # check the number of args
    if len(sys.argv) < 3:
        print('Usage: {} README.md README.html'.format(
            sys.argv[0]), file=sys.stderr)
        exit(1)
    if not os.path.exists(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        # print(lines)
        # parse/build html headings
        html = []
        uls = ['<ul>']
        has_ul = False
        ols = ['<ol>']
        has_ol = False
        paragraphs = []
        for index, line in enumerate(lines):
            st = line[:]  # make a copy just in case
            # check for ** (b) or __(em) and add to line
            if '_' in line:
                line = st[:st.find('_')] + '<em>' + st[st.find('_') +
                                                       2: st.rfind('_') - 1] + '<em/>' + st[st.rfind('_') + 1:]
            if '*' in line:
                line = st[:st.find('*')] + '<b>' + st[st.find('*') +
                                                      2: st.rfind('*') - 1] + '<b/>' + st[st.rfind('*') + 1:]
            # determine heading level and create element
            h_level = line.rfind('#')  # get last '#' index
            if h_level != -1:
                if h_level == 0:
                    html.append('<h1>' + line[h_level + 1:].strip() + '</h1>')
                if h_level == 1:
                    html.append('<h2>' + line[h_level + 1:].strip() + '</h2>')
                if h_level == 2:
                    html.append('<h3>' + line[h_level + 1:].strip() + '</h3>')
                if h_level == 3:
                    html.append('<h4>' + line[h_level + 1:].strip() + '</h4>')
                if h_level == 4:
                    html.append('<h5>' + line[h_level + 1:].strip() + '</h5>')
                if h_level == 5:
                    html.append('<h6>' + line[h_level + 1:].strip() + '</h6>')
            # parse Unordered listing syntax & create corresponding elements
            ul = line[0] == '-'
            if ul:
                has_ul = True
                uls.append('<li>' + line[1:].strip() + '</li>')
            # parse Ordered listing syntax & create corresponding elements
            ol = line[0] == '*'
            if ol:
                has_ol = True
                ols.append('<li>' + line[1:].strip() + '</li>')
            # parse paragraphs
            if h_level == -1 and not ul and not ol:
                # default to paragraph & check for empty lines & previous line
                if line not in ['\n', '\r', '\r\n']:
                    # if immediate previous line's a paragraph, add a <br/>
                    if len(paragraphs) and isParagraph(
                            lines[index - 1], h_level, ol, ul):
                        paragraphs[-1] = paragraphs[-1][:-5]
                        paragraphs.append('<br/>')
                        paragraphs.append(line.strip() + '</p>')
                    else:
                        paragraphs.append('<p>' + line.strip() + '</p> ')

        if has_ul:
            uls.append('</ul>')  # close <ul> list
        if has_ol:
            ols.append('</ol>')  # close <ol> list

        # print(html)
        lines = len(html)
        with open(sys.argv[2], 'a') as f:
            for idx, elem in enumerate(html):
                f.write(elem + '\n')  # add a new line at end of each line
            if has_ul:
                for idx, elem in enumerate(uls):
                    f.write(elem + '\n')
            if has_ol:
                for idx, elem in enumerate(ols):
                    f.write(elem + '\n')
            for paragraph in paragraphs:
                f.write(paragraph + '\n')
    exit(0)

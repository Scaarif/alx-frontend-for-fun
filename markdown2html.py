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
    # check the number of args
    if len(sys.argv) < 3:
        print('Usage: {} README.md README.html'.format(
            sys.argv[0]), file=sys.stderr)
        exit(1)
    if not os.path.exists(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)
    exit(0)

import sys
import datetime
from slugify import slugify

def make_frontmatter(title):
    current_day = datetime.datetime.today()
    formatted_date = datetime.date.strftime(current_day, '%m/%d/%Y %H:%M:%S %Z')

    frontmatter = """---
title: {0}
author: Chris
date: {1}
tags: 
---

Write content here.
""".format(title, formatted_date)

    return frontmatter

def make_template(title, frontmatter):
    file_name = slugify(title)

    with open(f'posts/{file_name}.md', 'w') as f:
        f.write(frontmatter)

def main(title):
    frontmatter = make_frontmatter(title)
    make_template(title, frontmatter)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Enter title of post.")
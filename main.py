import os
from markdown2 import markdown
from slugify import slugify
import jinja2

# TODO: Get markdown files/data
def get_files():
    posts = [f for f in os.listdir('posts') if os.path.isfile(os.path.join('posts', f))]
    return(posts)

# TODO: Convert to HTML
def get_post_content(posts):
    post_content = []
    for post in posts:
        with open(f'posts/{post}','r') as file:
            html_content = markdown(file.read(), extras=['metadata'])
            metadata = html_content.metadata
            metadata['slug'] = slugify(metadata['title'])
            post_data = {
                'title': metadata['title'],
                'slug': slugify(metadata['title']),
                'author': metadata['author'],
                'date': metadata['date'],
                'tags': list(metadata['tags'].split(", ")),
                'content': html_content
            }
            post_content.append(post_data)

    return(post_content)

# TODO: Save html to output directory
# TODO: Generate index
# TODO: Save style.css to '../output/static'
# TODO:

def main():
    posts = get_files()
    contents = get_post_content(posts)
    print(contents)


if __name__ == '__main__':
    main()
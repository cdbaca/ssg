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
            post_content.append({'metadata':metadata, 'content':html_content})

    return(post_content)

# TODO: Save html to output directory
# TODO: Generate index
# TODO: Save style.css to '../output/static'

def main():
    posts = get_files()
    print(get_post_content(posts))


if __name__ == '__main__':
    main()
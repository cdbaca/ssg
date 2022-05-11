import os
from markdown2 import markdown
from slugify import slugify
from jinja2 import Environment, PackageLoader, FileSystemLoader

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
            post_data = {
                'metadata':
                    {'title': metadata['title'],
                     'slug': slugify(metadata['title']),
                     'author': metadata['author'],
                     'date': metadata['date'],
                     'tags': list(metadata['tags'].split(", "))},
                'content': html_content
            }
            post_content.append(post_data)

    return(post_content)

# TODO: Save html to output directory
def make_posts(post_content):

    pass

# TODO: Generate index
def make_index(post_content):
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("index.html")

    post_metadata = []
    for post in post_content:
        post_metadata.append(post['metadata'])

    post_metadata.sort(key=lambda x: x['date'], reverse=True)

    rendered = template.render(data=post_metadata)

    os.makedirs('output', exist_ok=True)

    with open('output/index.html', 'w') as f:
        f.write(rendered)

# TODO: Save style.css to '../output/static'

def main():
    posts = get_files()
    post_content = get_post_content(posts)
    make_index(post_content)


if __name__ == '__main__':
    main()
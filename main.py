import os
from markdown2 import markdown
from slugify import slugify
from jinja2 import Environment, PackageLoader, FileSystemLoader

def get_files():
    posts = [f for f in os.listdir('posts') if os.path.isfile(os.path.join('posts', f))]
    return(posts)

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
                     'tags': list(metadata['tags'].split(", "))
                     },
                'content': html_content
            }
            post_content.append(post_data)

    return(post_content)

def make_posts(post_content):
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("post.html")

    for post in post_content:
        rendered = template.render(data=post)
        with open(f'output/{post["metadata"]["slug"]}.html', 'w') as f:
            f.write(rendered)

def make_index(post_content):
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("index.html")

    post_metadata = [post['metadata'] for post in post_content]
    post_metadata.sort(key=lambda x: x['date'], reverse=True)

    rendered = template.render(data=post_metadata)

    os.makedirs('output', exist_ok=True)

    with open('output/index.html', 'w') as f:
        f.write(rendered)

# TODO: make posts page
def make_about():
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("about.html")
    rendered = template.render()
    with open('output/about.html', 'w') as f:
        f.write(rendered)

# TODO: Save style.css to '../output/static'

# TODO: deal with tags
def run_tags(post_content):
    pass

# TODO: RSS feed
def make_rss():
    pass

def main():
    posts = get_files()
    post_content = get_post_content(posts)
    make_index(post_content)
    make_posts(post_content)
    make_about()
    run_tags(post_content)
    make_rss()

if __name__ == '__main__':
    main()
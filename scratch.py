import os, shutil
from markdown2 import markdown
from slugify import slugify
from jinja2 import Environment, PackageLoader, FileSystemLoader
import flickrapi
import page_data
import credentials
from copy import deepcopy

from datetime import datetime

def get_files():
    os.makedirs('posts', exist_ok=True)
    posts = [f for f in os.listdir('posts') if os.path.isfile(os.path.join('posts', f))]
    return(posts)

def sort(content, sortkey):
    content.sort(key=lambda x:x[sortkey], reverse=True)

def get_post_content(posts):
    post_content = []
    for post in posts:
        with open(f'posts/{post}','r') as file:
            html_content = markdown(file.read(), extras=['metadata'])
            metadata = html_content.metadata
            try:
                post_data = {
                    'metadata':
                        {'title': metadata['title'],
                        'slug': slugify(metadata['title']),
                        'author': metadata['author'],
                        'date': datetime.strptime(metadata['date'], "%m/%d/%Y %H:%S:%M"),
                        'tags': list(metadata['tags'].split(", "))
                        },
                    'content': html_content
                }
            except:
                post_data = {
                    'metadata':
                        {'title': metadata['title'],
                        'slug': slugify(metadata['title']),
                        'author': metadata['author'],
                        'date': datetime.strptime(metadata['date'], "%m/%d/%Y"),
                        'tags': list(metadata['tags'].split(", "))
                        },
                    'content': html_content
                }
            post_content.append(post_data)
    
    post_metadata = [post['metadata'] for post in post_content]
    sort(post_metadata, 'date')
    
    post_content.sort(key=lambda x:x['metadata']['date'], reverse=True)

    return(post_content, post_metadata)

if __name__ == '__main__':
    posts = get_files()
    post_content, post_metadata = get_post_content(posts)
    print(post_content)
    print(post_metadata)
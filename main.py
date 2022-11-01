import os, shutil
from markdown2 import markdown
from slugify import slugify
from jinja2 import Environment, PackageLoader, FileSystemLoader
import flickrapi
import credentials

def get_files():
    os.makedirs('posts', exist_ok=True)
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
        with open(f'docs/{post["metadata"]["slug"]}.html', 'w') as f:
            f.write(rendered)
        # print(post["metadata"]["tags"])

def get_imgs():
    key = credentials.key
    secret = credentials.secret
    user_id = '196813886@N05'

    flickr = flickrapi.FlickrAPI(key, secret, format='parsed-json')
    sets   = flickr.photosets.getList(user_id=user_id)
    set_id  = sets['photosets']['photoset'][0]['id']
    # set_info = flickr.photosets.getInfo(photoset_id=set_id)
    photo_info = flickr.photosets.getPhotos(photoset_id=set_id)
    photos_in_album = photo_info['photoset']['photo']

    photos = []

    for photo in photos_in_album:

        img_info = flickr.photos.getInfo(photo_id=photo['id'])

        img = 'https://live.staticflickr.com/{0}/{1}_{2}_q.jpg'.format(photo['server'], photo['id'], photo['secret'])
        img_link = 'https://www.flickr.com/photos/{0}/{1}/in/album-{2}/'.format(user_id, photo['id'], set_id)
        
        photos.append({'title':photo['title'], 'date_created':img_info['photo']['dateuploaded'], 'img_link':img_link, 'img':img})
        photos.sort(key=lambda x:x['date_created'], reverse=True)

    return(photos)


def make_index(post_content, photo_data):
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("index.html")

    post_metadata = [post['metadata'] for post in post_content]
    post_metadata.sort(key=lambda x: x['date'], reverse=True)

    content = {}

    content['posts'] = post_metadata
    content['photos'] = photo_data

    rendered = template.render(data=content)

    os.makedirs('docs', exist_ok=True)

    with open('docs/index.html', 'w') as f:
        f.write(rendered)

def make_about():
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("about.html")
    rendered = template.render()
    with open('docs/about.html', 'w') as f:
        f.write(rendered)

def make_css():
    os.makedirs('docs/static', exist_ok=True)
    shutil.copy('static/styles.css', 'docs/static')
    shutil.copy('static/github.png', 'docs/static')

def run_tags(post_content):
    blog_tags = [post['metadata']['tags'] for post in post_content if post['metadata']['tags'][0] != '']
    tag_dict = {}
    for tag_list in blog_tags:
        for tag in tag_list:
            if tag not in tag_dict:
                tag_dict[tag] = 1
            else:
                tag_dict[tag] += 1

    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("tags.html")
    rendered = template.render(data=tag_dict)
    with open('docs/tags.html', 'w') as f:
        f.write(rendered)

    os.makedirs('docs/tags', exist_ok=True)

    tag_post_dict = {}

    for k,v in tag_dict.items():
        for post_data in post_content:
            if k in post_data['metadata']['tags']:
                if k not in tag_post_dict:
                    tag_post_dict[k] = [[
                                    post_data['metadata']['title'],
                                    post_data['metadata']['slug'],
                                    post_data['metadata']['date']
                                    ]]
                else:
                    tag_post_dict[k].append([
                                    post_data['metadata']['title'],
                                    post_data['metadata']['slug'],
                                    post_data['metadata']['date']
                                    ])
        # THE PROBLEM WITH THIS METHOD IS THAT I CANNOT PASS THE TAG TITLE INTO THE HTML (SEE DATA=TAG_POST_DICT[K])
        template = env.get_template("single_tag.html")
        rendered = template.render(data=tag_post_dict[k])
        with open(f'docs/tags/{k}.html', 'w') as f:
             f.write(rendered)

# TODO: RSS feed
def make_rss():
    pass

def main():
    posts = get_files()
    post_content = get_post_content(posts)
    photo_data = get_imgs()
    make_index(post_content, photo_data)
    make_posts(post_content)
    make_about()
    make_css()
    run_tags(post_content)
    make_rss()

if __name__ == '__main__':
    main()
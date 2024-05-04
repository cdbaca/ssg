import os, shutil
from markdown2 import markdown
from slugify import slugify
from jinja2 import Environment, PackageLoader, FileSystemLoader
import flickrapi
import page_data
import credentials
from copy import deepcopy

from datetime import datetime

MENU = page_data.menu
LINKS = page_data.links

PAGES = ['about', 'lift']
LISTPAGES = {'posts':None, 'photos':None}
STATICDIR = 'docs/static'
TEMPLATESDIR = './templates'
  
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

def make_posts(post_content):
    env = Environment(loader=FileSystemLoader(TEMPLATESDIR))
    template = env.get_template("post.html")

    for post in post_content:
        rendered = template.render(data=post, menu=MENU)
        with open(f'docs/{post["metadata"]["slug"]}.html', 'w') as f:
            f.write(rendered)

def sort(content, sortkey):
    content.sort(key=lambda x:x[sortkey], reverse=True)

def get_imgs():
    key = credentials.key
    secret = credentials.secret
    user_id = '196813886@N05'

    flickr = flickrapi.FlickrAPI(key, secret, format='parsed-json')
    sets   = flickr.photosets.getList(user_id=user_id)
    set_id  = sets['photosets']['photoset'][0]['id']
    photo_info = flickr.photosets.getPhotos(photoset_id=set_id)
    photos_in_album = photo_info['photoset']['photo']

    photos = []

    for photo in photos_in_album:

        img_info = flickr.photos.getInfo(photo_id=photo['id'])

        img = 'https://live.staticflickr.com/{0}/{1}_{2}_q.jpg'.format(photo['server'], photo['id'], photo['secret'])
        img_link = 'https://www.flickr.com/photos/{0}/{1}/in/album-{2}/'.format(user_id, photo['id'], set_id)
        
        photos.append({'title':photo['title'], 'date_created':img_info['photo']['dateuploaded'], 'img_link':img_link, 'img':img})

    sort(photos, 'date_created')   

    # only get 4 most recent photos
    recent_photos = []
    for i in range(0, 4):
        recent_photos.append(photos[i])

    return(recent_photos, photos)

def make_now():
    os.makedirs('now', exist_ok=True)
    
    with open(f'now/now_page.md','r') as file:
        html_content = markdown(file.read())

    env = Environment(loader=FileSystemLoader(TEMPLATESDIR))
    template = env.get_template('now.html')

    content = {}
    content['html_content'] = html_content

    rendered = template.render(data=content, menu=MENU)

    os.makedirs('docs', exist_ok=True)

    with open('docs/now.html', 'w') as f:
        f.write(rendered)
        

def make_index(post_metadata, photo_data):
    env = Environment(loader=FileSystemLoader(TEMPLATESDIR))
    template = env.get_template("index.html")

    # only get 10 most recent posts
    copy_metadata = deepcopy(post_metadata)
    recent_posts = []
    for i in range(0, 10):
        post = copy_metadata[i]

        date = post['date']

        try:
            date = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
            post['date'] = date.strftime('%m/%d/%Y')
        except:
            post['date'] = date.strftime('%m/%d/%Y')
        
        recent_posts.append(post)

    content = {}

    content['posts'] = recent_posts
    content['photos'] = photo_data

    rendered = template.render(data=content, menu=MENU, links=LINKS)

    os.makedirs('docs', exist_ok=True)

    with open('docs/index.html', 'w') as f:
        f.write(rendered)

def make_pages(page_name, *args):
    env = Environment(loader=FileSystemLoader(TEMPLATESDIR))
    template = env.get_template(f"{page_name}.html")

    if args:
        rendered = template.render(data=args[0], menu=MENU)
    else:
        rendered = template.render(menu=MENU)

    with open(f'docs/{page_name}.html', 'w') as f:
        f.write(rendered)

def make_static():
    os.makedirs(STATICDIR, exist_ok=True)
    shutil.copy('static/styles.css', STATICDIR)
    shutil.copy('static/calc.js', STATICDIR)

def run_tags(post_content):
    blog_tags = [post['metadata']['tags'] for post in post_content if post['metadata']['tags'][0] != '']
    tag_dict = {}
    for tag_list in blog_tags:
        for tag in tag_list:
            if tag not in tag_dict:
                tag_dict[tag] = 1
            else:
                tag_dict[tag] += 1

    env = Environment(loader=FileSystemLoader(TEMPLATESDIR))
    template = env.get_template("tags.html")
    rendered = template.render(data=tag_dict, menu=MENU)
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
        rendered = template.render(data=tag_post_dict[k], menu=MENU)
        with open(f'docs/tags/{k}.html', 'w') as f:
             f.write(rendered)

def make_rss(post_content):
    env = Environment(loader=FileSystemLoader(TEMPLATESDIR))
    template = env.get_template("feed.xml")
    
    feed_posts = deepcopy(post_content)
    feed_post_list = []
    for i in range(0, 5):
        post = feed_posts[i]
        
        date = feed_posts[i]['metadata']['date']
        try:
            date = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
            feed_posts[i]['date'] = date.strftime('%m/%d/%Y %H:%M:%S')
        except:
            feed_posts[i]['date'] = date.strftime('%m/%d/%Y') + " 00:00:00"
        
        feed_post_list.append(post)

    rendered = template.render(data=feed_post_list)

    os.makedirs('docs', exist_ok=True)

    with open('docs/feed.xml', 'w') as f:
        f.write(rendered)

def main():
    posts = get_files()
    post_content, post_metadata = get_post_content(posts)

    print("got posts")
    
    recent_photos, photos = get_imgs()

    print("got images")

    make_now()

    print("made now")

    make_index(post_metadata, recent_photos)

    make_posts(post_content)

    LISTPAGES['photos'] = photos
    LISTPAGES['posts'] = post_metadata

    for page_name in PAGES:
        make_pages(page_name)

    for page_name, content in LISTPAGES.items():
        make_pages(page_name, content)

    make_static()

    print("made static")

    run_tags(post_content)

    print("made tags")

    make_rss(post_content)

    print("made rss")

if __name__ == '__main__':
    main()
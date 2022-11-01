---
title: Adding a Photos Feature
author: Chris
date: 11/01/2022
tags: python, open web
---

In my spare time today and yesterday, I spent some time attempting to get a photo feed on the site. So far, I've been successful, at least with the "getting it working" part. (See the home page). It's not yet the prettiest thing in the world, but I was pretty happy that I was able to get it working.

This was brought on by continued thinking about open web stuff. If Twitter sucks (it does) and Facebook sucks (it *definitely* does), Instagram isn't far behind. My experience on Instagram has been relatively shitty anyway. There are more advertisements, the feed hasn't been chronological in a long time, and everyone just uses stories now instead of the regular photo posting functionality. I get it. That's what they're trying to push as a TikTok competitor. But I really, *really* hate TikTok. It seems to me to be peak bad internet. It's algorithm attention-grabbing at its very worst.

[The internet wasn't supposed to be a consumer hell hole](https://cheapskatesguide.org/articles/reflections-on-the-internet.html). It was meant to be a way to share information, gain knowledge, make connections we couldn't have otherwise made. I want to continue to do my part in making it closer to that ideal and less the content machine that it has become.

For the photos feature, I decided to use Flickr as a photo host, and I'm using their API and the [FlickrAPI library](https://stuvel.eu/software/flickrapi/) to get the necessary information to produce both the image, the link to the image in the album, and the title of the image. There's a little bit of sorting magic going on, and I'm sure if I change anything about how my Flickr albums are used, I'll have to adjust the code. But I'm happy with the function:

`

    def get_imgs():
        key = credentials.key
        secret = credentials.secret
        user_id = 'credentials.user_id'

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
            photos.sort(key=lambda x:x['date_created'], reverse=True)

        return(photos)
        
`

Then I take that data, throw it in a dictionary for an index function that produces the home page, and use that to render the images. Pretty cool.

Back to yesterday's point... this clearly doesn't "reproduce" Instagram in any way. You lose some follow-ability here, and I'm obviously not trying to make some clone with captions, likes, comments, or stories. But it is a way to just put up what I'm doing and who I want to be in the digital space. If we could be happy enough with stuff like this, I think we'd all be better off.
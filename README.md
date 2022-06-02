# The copycat ssg

I miss blogging. For the last year, my focus has been learning sql, some data analysis/report writing, 
and Python for work. This has been fun, but I want/need to work on other aspects of my life too.

While I'm familiar with Blogger, Wordpress, and other CMSs that allow you to just "plug and play", I'm not really
interested in the bloat that comes with those systems. So, to combine the programming skills that I've gained,
this project is just a small attempt to do something new/different/quirky. And hopefully respark a love of blogging
and writing again.

Static site generators are pretty basic. The idea is simple:
- Have a directory with markdown files
- Convert those files into HTML, and input that content into a template generator like Jinja
- Put the index, post files, and static files (like CSS) into the output directory
- Serve those files up on a server like Github pages or whatever.

There's a ton out there on SSGs. Here are the different tutorials I'm using for guidance:
- https://www.megacolorboy.com/posts/build-your-own-static-site-generator-using-python/
- https://rahmonov.me/posts/static-site-generator/
- https://blog.hamaluik.ca/posts/build-your-own-static-site-generator/
- https://blog.thea.codes/a-small-static-site-generator/
- https://www.youtube.com/watch?v=fe8QgK3j4gw&lc=UgzXwbW2XiYbibiUxj94AaABAg.9arQ0nNBndd9arVdRDcKub

If you want your own version, you can clone the repository. Obviously, you'd want to delete any posts in the 
posts directory, and delete the entire 'docs' directory.

From there, to generate a new post, you can run:

`python3 post.py "Input Post Title"`

After writing your blog post, in that Markdown file (and changing the frontmatter of the post), save the file.

Once it's saved, you should be able to run:

`python3 main.py`

This will generate the HTML files for the blog, including the index, about, and tags page.

If you're using GitHub pages to host the site, you can simply change the top directory (ssg) to a git 
repository. Then head over to the settings of the repo in GitHub, click "Pages", and activate GitHub Pages for the repo. 
[More info on that process here.](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

You can see my own version of [this blog](https://cdbaca.github.io/ssg/) here.

# Future Goals:

- Generate a page that is instagram/micro.blog-like which allows me to post pictures
- Generate a Now page
- Make an RSS feed
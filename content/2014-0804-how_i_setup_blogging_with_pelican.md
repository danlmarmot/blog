Title: How I setup blogging with Pelican
Date: 2014-08-03 18:55
Tags: pelican
Category: Tech
Slug: blog-setup-with-pelican
Summary: A howto on setting up Pelican

For a long while, I've wanted to move to a decent blogging system.  I tried WordPress, but keeping it up-to-date with patches and running MySQL for content just seemed kind of wrong--I wanted something simpler and version controlled and not tied to particular server setup, so eventually I found my way to Pelican.

And, following the unwritten mandatory rule that the first blog post should be about how a blog is setup, I present you with the magic "How I setup blogging with Pelican" post :-).

I still have theming to do, but that's a different post than this one.

### Getting going

For this blog, I'm using Pelican 3.4.0, and Github pages.

I spent probably far too much time looking around at other tutorials and resources out there.--these two pages gave me enough insight on how to do this:

[http://guizishanren.com/guide-to-set-up-github-page-and-pelican](http://guizishanren.com/guide-to-set-up-github-page-and-pelican)

[http://www.circuidipity.com/pelican.html](http://www.circuidipity.com/pelican.html) 

**A small aside**: many tutorials are aimed more at writers than developers, and they struggle a bit with the concept of git branching and pushing.  Some suggest two different repositories are needed, but that's not necessary--just use a single Github repo with your editable content in the branch "master" and your static, hosted blog content in "gh-pages".  Github pages knows to serve static content out of any branch named "gh-pages".

There's a plugin that helps you generate that static content, so you never have to switch branches either--you always work in master.

## Setting up Pelican

Resources for working with Pelican and Github: http://docs.getpelican.com/en/3.4.0/tips.html are pretty good.  

I'm using a Mac running MacOS 10.9, and my setup looks like this:

- The blog's content and scripts and everything will live in my home directory at ~/dev/blog
- All the Python stuff will be in a virtual environment, also kept in that same directory and .gitignore'd.
- I'll be writing posts in Markdown with Mou.
- The blog will be hosted on Github as a project page (not a personal or user page--this is an important distinction)

### Install Pelican

Open a terminal window and enter these commands to install Pelican, Markdown, and ghp-import

```
sudo easy_install pip; sudo pip install virtualenv
mkdir ~/dev/blog; cd $_
virtualenv venv; . venv/bin/activate
pip install pelican Markdown ghp-import
```
### Run the Pelican Quickstart
Most questions I accepted the default, except the pagination and Github one.

```
pelican-quickstart

> Where do you want to create your new web site? [.]
> What will be the title of this web site? Dan's Random Bits
> Who will be the author of this web site? Dan McKean
> What will be the default language of this web site? [en]
> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) Y
> What is your URL prefix? (see above example; no trailing slash) https://danlmarmot.github.io/blog

-- Note this change from default for pagination
> Do you want to enable article pagination? (Y/n) n
> How many articles per page do you want? [10]
> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n)
> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n)
> Do you want to upload your website using FTP? (y/N)
> Do you want to upload your website using SSH? (y/N)
> Do you want to upload your website using Dropbox? (y/N)
> Do you want to upload your website using S3? (y/N)
> Do you want to upload your website using Rackspace Cloud Files? (y/N)

-- Note this is yes for Github pages.
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) N
Done. Your new project is available at ~/dev/blog

```

### Initial Pelican Run
This will generate your blog and run a webserver to view your content.

`make devserver`

Open [http://localhost:8000](http://localhost:8000) when it's finished to see what your blog looks like.

**Note**:
On a second runthrough of these steps, I had an old instance of the devserver running.  Stop it and/or clean up its stale old pidfile with this command:

`./develop_server.sh stop`

### Write a blog post!
Now let's create that first post.  Make sure that terminal window's still open to that directory.  You can have the command prompt, that's fine.

Open Mou. If you don't have Mou, install it from http://mouapp.com/ 

Create a file named "2014-0803.md" in the content directory, and add this text:  

```
Title: First Post!
Date: 2014-08-03 12:50
Tags: fun
Category: Tech
Slug: my-first-post
Summary: First Post to blog

# Hey, an initial blog post.

Just getting started.  More to come.
```

Save it away as "2014-0803.md" inside of your  /content … and your site will magically (and weirdly!) regenerate.

View it at [http://localhost:8000](http://localhost:8000) again--or just refresh the page if you left your browser window open.   You may need to refresh.


## Add Git

Now let's put this blog under git on your local machine... and then we'll push your local git repository to Github.

###Create a local git repo

In that same directory at ~/dev/blog, create a local Git repo, and a .gitignore file, and then add content and associated files:

```
git init
echo -e "venv\n*.pyc\n*.pid\noutput/\ncache\n" > .gitignore
git add .
git status
```

Make sure additional files aren't being checked in.  Mine looks like this:

```
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

	new file:   .gitignore
	new file:   Makefile
	new file:   content/2014-0803.md
	new file:   develop_server.sh
	new file:   fabfile.py
	new file:   pelicanconf.py
	new file:   publishconf.py
```
Commit to your local Git repo

```
git commit -m "Initial checkin"
```

### Create a Github repo to hold your blog.
Visit [https://github.com/new](https://github.com/new), and call it just "blog".  Make it public.  And you don't need to add a ReadMe.md, but if you do point it to your Github pages blog.

### Add Github as a remote repository
Now we can add Github as a remote repository.  We will push changes when we're satisfied with them.

```
git remote add origin https://github.com/danlmarmot/blog.git
```

Push the current changes.  You'll need to do this longform command with the "-u origin master" for this very first push, by the way.   Later commits you can just do "git push origin master"

```
git push -u origin master
```

### Push to Github
This part's easy, and this is what you need to do to update your blog.

```  
make github
```

And then view it on Github:  [https://danlmarmot.github.io/blog/](https://danlmarmot.github.io/blog/).  Note that it might take up to ten minutes for the blog to show up.

If you haven't used Git much, a good way to think of this pushing to Github as nothing more than sending updates to Github--don't think of Github as an authoritative source for your blog or some old-school master source code control server.  You're just telling Github that you're pushing new static content to it, generated on your own machine.  The real content is kept both on your machine and Github in the master branch.

As for the gh-pages branch, you can somewhat ignore it.  It's almost a build artifact, rather than a real source code/content branch that you directly manipulate.

### Lastly, a few notes on where this leaves your repository.

When you do this, you'll be left on your master branch, and not the gh-pages branch.  In Github, you'll have two separate branches with no common ancestor node, which looks kind of weird but is fine.
Github has a set of instructions at https://pages.github.com, but to be honest you don't ever need to go there--you can do everything from the command line once you make your Github repo.

That's all folks!




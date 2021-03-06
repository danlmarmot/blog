#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Dan McKean'
SITENAME = u"Dan's Random Bits"
SITEURL = 'http://localhost:8000'

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         # ('Python.org', 'http://python.org/'),
         # ('Jinja2', 'http://jinja.pocoo.org/'),
         # ('You can modify those links in your config file', '#')
         )

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = False
PATH_METADATA = r'(?P<date>\d{4}\/\d{2}\/\d{2})-(?P<slug>.*)'

SUMMARY_MAX_LENGTH = 50

#THEME='pelican-themes/elegant'
THEME = 'pelican-themes-custom/pelican-bootstrap3'
# taken from Dandydev.net
BOOTSTRAP_THEME = 'readable'
#BOOTSTRAP_THEME = 'simplex'
#BOOTSTRAP_THEME = 'journal'
DISQUS_SITENAME = "dansrandombits-dev"

# Date-based URLs for posts
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Indexes for data-based URLs
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'
DAY_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/index.html'
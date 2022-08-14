AUTHOR = 'evilchili'
SITENAME = 'The Dead Sands'
SITEURL = 'https://deadsands.froghat.club/'
RELATIVE_URLS = False
THEME = 'deadsands-theme'

SLUGIFY_SOURCE = 'basename'

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'
DEFAULT_DATE = 'fs'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

ARTICLE_URL = '{category}/{slug}/'
CATEGORY_URL = "{slug}/index.html"
TAG_URL = "tags/{slug}/"
AUTHOR_URL = "{slug}/"
PAGE_URL = '{slug}/'
ARCHIVES_URL = "archives/"

ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
CATEGORY_SAVE_AS = "{slug}/index.html"
TAG_SAVE_AS = "tags/{slug}/index.html"
AUTHOR_SAVE_AS = "{slug}/index.html"
PAGE_SAVE_AS = '{slug}/index.html'

TAGS_SAVE_AS = "tags/index.html"
CATEGORIES_SAVE_AS = "category/index.html"
ARTICLES_SAVE_AS = '{category}/index.html'
PAGES_SAVE_AS = "pages/index.html"

ARCHIVE_SAVE_AS = "archives/{slug}.html"
ARCHIVES_SAVE_AS = "archives/index.html"

MENU_ITEMS = (
    ("Index", "archives/"),
)

SITEMAP = {
    'format': 'xml',
    "exclude": ["tag/"],
}

PLUGINS = [
    'yaml_metadata',
    'sitemap',
]

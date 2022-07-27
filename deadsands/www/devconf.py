AUTHOR = 'evilchili'
SITENAME = 'The Dead Sands'
SITEURL = 'http://localhost:8000'
RELATIVE_URLS = True
THEME = 'deadsands-theme'

DISPLAY_PAGES_ON_MENU = True

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None
# AUTHOR_FEED_ATOM = None
# AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10


ARTICLE_URL = '{category}/{slug}/'
CATEGORY_URL = "{slug}/"
TAG_URL = "tags/{slug}/"
AUTHOR_URL = "{slug}/"
PAGE_URL = '{slug}/'

ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
CATEGORY_SAVE_AS = "{slug}/index.html"
TAG_SAVE_AS = "tags/{slug}/index.html"
AUTHOR_SAVE_AS = "{slug}/index.html"
PAGE_SAVE_AS = '{slug}/index.html'

TAGS_SAVE_AS = "tags/{slug}/index.html"
CATEGORIES_SAVE_AS = "category/index.html"
ARTICLES_SAVE_AS = '{category}/index.html'
PAGES_SAVE_AS = "pages/index.html"

ARCHIVES_URL = ""
ARCHIVE_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""

MENU_ITEMS = (
    ('Sessions', 'sessions'),
    ('Lore', 'lore'),
    ('Beastiary', 'beastiary'),
    ('Tags', 'tags'),
)


PLUGINS = [
    'yaml_metadata',
    'drafts',
]

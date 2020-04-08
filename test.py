import wikipediaapi
from pyre2 import re2
wiki_wiki = wikipediaapi.Wikipedia('en')

page_py = wiki_wiki.page('Dog')
print(page_py.text)
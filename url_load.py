import urllib
import os
from urlparse import urlparse

testfile = urllib.URLopener()
path = "https://farm1.static.flickr.com/744/21456282281_581c0dba50.jpg"
parsed_address = urlparse(path)

testfile.retrieve("https://farm1.static.flickr.com/744/21456282281_581c0dba50.jpg", "21456282281_581c0dba50.jpg")
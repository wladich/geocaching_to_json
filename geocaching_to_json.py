# coding: utf-8
from lxml import etree, objectify
from lxml import html
import json
import urllib2
import sys


kml_url = 'http://www.geocaching.su/kml/kml_lite.php'

def convert(filename):
    f = urllib2.urlopen(kml_url)
    root = etree.parse(f).getroot()
    for elem in root.getiterator():
        i = elem.tag.index('}')
        if i > 0:
            elem.tag = elem.tag[i + 1:]

    caches = []
    for placemark in root.xpath('.//Placemark'):
        name = placemark.find('name').text.strip()
        coords = placemark.xpath('.//coordinates')[0].text
        lng, lat = map(float, coords.split(','))
        description = placemark.find('description').text
        description = html.fragment_fromstring(description, create_parent=True)
        url = description.xpath('.//a')[0].attrib['href']
        caches.append([name.encode('utf-8'), url.encode('utf-8'), lat, lng])
    with open(filename, 'w') as f:
        json.dump(caches, f, ensure_ascii=False)



if __name__ == '__main__':
    output_filename, = sys.argv[1:]
    convert(output_filename)
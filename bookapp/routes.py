from flask import render_template
import re
from bs4 import BeautifulSoup
from bookapp import app

def parse_htmlbook():
    page = render_template('senseandsensibility.html')
    links = get_chap_links(page)
    sections = {}
    for ind in range(len(links)):
        section = {}
        start = links[ind]
        if ind < len(links)-1:
            end = links[ind+1]
            patt = ('<a name="{}"></a>(.*)' + '<a name="{}"></a>').format(start,end)
            match = re.search(patt,page,re.MULTILINE|re.DOTALL)
        else:
            patt = '<a name="{}"></a>(.*)<pre>'.format(start)
            match = re.search(patt,page,re.MULTILINE|re.DOTALL)
        if match:
            soup = BeautifulSoup(match.group(1))
            plist = [p.contents[0] for p in soup.find_all('p')]
            section['title']= (soup.find('h2').contents)[0]
            section['plist']= plist
            sections[start] = section
    return links, sections

def get_chap_links(page):
    soup = BeautifulSoup(page)
    links = [str(link.get('href'))[1:]
             for link in soup.find_all('a') if link.get('href')]
    return links

@app.route('/')
def index():
    links, sections = parse_htmlbook()
    chapter = len(links)
    title = "Sense and Sensibility by Jane Austen"
    section = []
    for i in range(chapter):
        section.append(str(sections[links[i]]['title']))
    image_url = '/static/images/title_img.jpg'
    return render_template('index.html', title = title, image_url = image_url, section = section, n = chapter, links = links)


@app.route('/<page>')
def section(page):
    links, sections = parse_htmlbook()
    chapter = len(links)
    title=sections[links[int(page)]]['title']
    section = []
    p = []
    for i in range(chapter):
        section.append(str(sections[links[i]]['title']))
    p = sections[links[int(page)]]['plist']
    return render_template('section.html', n = chapter, section = section, title = title, paragraphs = p)



import requests
import re
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime as dt

# all_tags = SoupStrainer(id=['menu', 'Printable', 'after_section_1', 'page-42', 'textwidget'])



urls = {
    'Amica Tellus': "http://www.lounaat.info/lounas/amica-tellus/helsinki",
    # 'POR': "http://www.por.fi/Menu-Pitajanmaki",
    # # 'Theron': "http://eatwork.fi/tilat/valimotie-27/",
    # 'Theron': "https://www.lounaat.info/lounas/theron-catering-pitjnmki/helsinki",
    # 'Factory': "http://www.ravintolafactory.com/lounasravintolat/ravintolat/helsinki-pitajanmaki/",
    # # 'Blancco': "http://www.ravintolablancco.com/lounas-ravintolat/pitajanmaki/",
    # 'Blancco': "https://www.lounaat.info/lounas/blancco-pitajanmaki/helsinki",
    # # 'Smarteat': "http://www.smarteat.fi/menu-pitskun-kanttiini/",
    # 'Smarteat': "https://www.lounaat.info/lounas/smarteat-pitsku/helsinki",
    # 'Amica Lasihelmi': "http://www.lounaat.info/lounas/amica-lasihelmi/helsinki",
}

WEEKDAYS = [
    "maanantai",
    "tiistai",
    "keskiviikko",
    "torstai",
    "perjantai",
    "lauantai",
    "sunnuntai"
]


def weekday_str():
    return WEEKDAYS[dt.today().weekday()]


def parse(html_txt, weekday, restaurant):
    amica_tags = SoupStrainer(id='menu')
    tag = amica_tags        # Default to lounaat.info
    if (restaurant == 'POR'):
        por_tags = SoupStrainer(id='Printable')
        tag = por_tags
    # elif (restaurant == 'Theron'):
    #     theron_tags = SoupStrainer(id='after_section_1')
    #     tag = theron_tags
    elif (restaurant == 'Factory'):
        factory_tags = SoupStrainer(id='main') # Fix
        tag = factory_tags
    # elif (restaurant == 'Blancco'):
    #     blancco_tags = SoupStrainer(id='page-42')     # Fix
    #     tag = blancco_tags
    # elif (restaurant == 'Smarteat'):
    #     smarteat_tags = SoupStrainer(id='textwidget') # Fix
    #     tag = smarteat_tags
    soup = BeautifulSoup(html_txt, 'html.parser', parse_only=tag)


    if (restaurant == 'POR'):
        pass
    # elif (restaurant == 'Theron'):

    elif (restaurant == 'Factory'):
        pass
    # elif (restaurant == 'Blancco'):
 
    # elif (restaurant == 'Smarteat'):

    else:
        # items = soup.find_all("h3")
        return soup.find(lambda tag: tag.name == "h3" and tag.text.lower().startswith(weekday)).parent.parent.prettify()
    return soup.prettify()


def main():
    wd = weekday_str()
    # print(wd)
    for (name, url) in urls.items():
        resp = requests.get(url)
        print("{0}: {1}".format(name, resp.status_code))
        text = parse(resp.text, wd, name)
        # print(text)
        with open("test.html", 'a', encoding='utf-8') as f:
            f.write(text)
            # pass


main()

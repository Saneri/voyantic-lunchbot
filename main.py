import requests
import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime as dt
from datetime import timedelta

load_dotenv()
SLACK_URL = 'https://slack.com/api/chat.postMessage'
CHANNEL = os.getenv('SLACK_CHANNEL')
print(str(CHANNEL))
TOKEN = os.getenv('SLACK_TOKEN')
HEADERS = {
    'content-type': 'application/json',
    'authorization': f'Bearer {TOKEN}'
}

URLS = {
    'Knitter': "https://www.lounaat.info/lounas/knitter/espoo",
    'Bluebell': "https://www.lounaat.info/lounas/bluebell/espoo",
    'Happy Friends': "https://www.lounaat.info/lounas/happy-friends/espoo",
    'Sodexo Täyttymys': "https://www.lounaat.info/lounas/sodexo-tyttymys/espoo",
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


def weekday_int():
    return dt.today().weekday()


def parse(html_txt, weekday, restaurant):
    try:
        amica_tags = SoupStrainer(id='menu')
        tag = amica_tags        # Default to lounaat.info
        if (restaurant == 'Factory'):
            # Load whole page since Factory has no good ids to parse into
            soup = BeautifulSoup(html_txt, 'html.parser')
            # Find parent of lounaslista text, which holds whole week in
            # multiple <p>'s (*sigh :( )
            s = soup.find(lambda tag: tag.name == "h2" and tag.text.lower(
            ).startswith("lounaslista")).parent.text
            # Find today and tomorrow from the huge string which has whole week
            # lunch and some bloat text
            s = (s[s.lower().find(weekday) +
                   len(weekday):s.lower().find(WEEKDAYS[(dt.today() +
                                                         timedelta(days=1)).weekday()])])
            # Get rid of date text that is following the weekday and return the
            # text
            s = (s[s.find("\n") + len("\n"):])
            return s
        else:       # lounaat.info parse
            soup = BeautifulSoup(html_txt, 'html.parser', parse_only=tag)
            raw_html = soup.find(lambda tag: tag.name == "h3" and tag.text.lower(
            ).startswith(weekday)).parent.parent
            lst = []
            for elem in raw_html.find_all("p"):
                if not elem.text.startswith("Mixed lunch:")\
                        and not elem.text.startswith("Kaikki lounaspakettimme sisältävät")\
                        and not elem.text.startswith("All of our lunch options"):
                    lst.append(" ".join(elem.text.split()))
            return '\n'.join(lst)
    except Exception:
        return ""       # Default failed parse


def main():
    wd = weekday_str()
    ret = json.loads(requests.post(SLACK_URL, data=json.dumps(
        {
            'token': TOKEN,
            'channel': CHANNEL,
            'text': f'Lounaat {wd}',
            'charset': 'utf8'
        }
    ), headers=HEADERS).text)
    print(str(ret))
    thread_id = ret['ts']
    for (restaurant, url) in URLS.items():
        try:
            resp = requests.get(url)
            print("{0}: {1}".format(restaurant, resp.status_code))
            text = parse(resp.text, wd, restaurant)
            bolded_header = "*{0}:*\n".format(restaurant)
            data = {
                'text': bolded_header + text,
                'channel': CHANNEL,
                'thread_ts': thread_id,
            }
            ret = json.loads(
                requests.post(
                    SLACK_URL,
                    data=json.dumps(data),
                    headers=HEADERS).text)
        except Exception as ex:
            print(ex)
            requests.post(SLACK_URL, data=json.dumps(
                {'text': ex}), headers=HEADERS)


main()

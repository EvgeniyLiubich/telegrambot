from lxml import etree
import requests
from io import StringIO
import json


def get_random_film():
    response = requests.get('https://www.kinopoisk.ru/index.php?kp_query=%D1%88%D1%80%D0%B5%D0%BA')

    parser = etree.HTMLParser()

    tree = etree.parse(StringIO(str(response.content)), parser=parser)

    l_list = tree.xpath('//span[@class="name"]/text()')
    l_list2 = tree.xpath('//div[@class="pic"]/a/@href')


    film_name = l_list[0].encode('ascii').decode('unicode-escape').encode('iso-8859-1').decode('utf-8')
    link_film = 'https://www.kinopoisk.ru/' + l_list2[0]

    film_listt = [film_name, link_film]
    return film_listt




# with open('kinopoisk.json', 'w+') as f:
#     f.write(json.dump(result_list, f, indent=2))

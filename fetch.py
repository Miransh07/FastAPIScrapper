import requests
from bs4 import BeautifulSoup


def fetch(url):
    # url = 'https://github.com/trending'
    sess = requests.Session()
    response = sess.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Repository name
    #Description
    #No. of stars
    #No. of forks
    #Language
    #Topic/Tags
    lst = []
    for box in soup.find_all('article', class_='Box-row'):
        d = {}
        repo = box.find('h2', class_= 'h3 lh-condensed')
        repo_name = repo.get_text(strip=True)
        add = ""
        for i in repo_name:
            if i !=  " ":
                add += i
        new_url = 'https://github.com/' + add
        # print(new_url)
        # m = repo_name.split('/')[-1]
        d['id'] = repo_name
        Desc = box.find('p').get_text(strip=True)
        d['Desc'] = Desc

        a_tag = box.find_all('a', class_='Link Link--muted d-inline-block mr-3')
        stars = a_tag[0].get_text(strip=True)
        d["Stars"] = stars
        forks = a_tag[-1].get_text(strip=True)
        d['Forks'] = forks
        lang_tag = box.find('span', class_="d-inline-block ml-0 mr-3")
        if lang_tag:
            lang = lang_tag.get_text(strip=True)
        else:
            lang = 'Not specified'
        d['Language'] = lang
        # topics = box.find('')
        new_response = sess.get(new_url)
        new_soup = BeautifulSoup(new_response.text, 'html.parser')
        # print(new_soup)
        another_new_soup = new_soup.find('div', class_='Layout-sidebar')
        # print(another_new_soup)
        topic_box = another_new_soup.find('div', class_='f6')
        topic = set()
        if topic_box:
            for i in topic_box.find_all('a'):
                # print(i.get_text(strip=True))
                topic.add(i.get_text(strip=True).lower())

        d['Topics'] = topic
        # print(d['id'])
        lst.append(d)

    return lst


def get_connections(data):
    # print('here now, get')
    output = {}
    output['nodes'] = []
    output['edges'] = []

    for x in data:
        output['nodes'].append(x)
        for y in data:
            if x != y:
                a = output.get('edges', [])
                flag = False
                for dic in a:
                    temp = [dic['source'], dic['target']]
                    if x['id'] in temp and y['id'] in temp:
                        flag = True
                        break

                if not flag:
                    weight = len(x['Topics'].intersection(y['Topics']))
                    if weight != 0:
                        output['edges'].append(
                            {
                                'source': x['id'],
                                'target': y['id'],
                                'weight': weight,
                            }
                        )
    # print('done get')
    return output
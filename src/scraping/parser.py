import codecs
from random import randint
from bs4 import BeautifulSoup as BS
import requests

__all__ = ('workSite', 'rabotaSite', 'dou', 'djinni')

header = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
]


def workSite(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=header[randint(0, 3)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def rabotaSite(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    if url:
        resp = requests.get(url, headers=header[randint(0, 3)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('div',
                                 attrs={'class': 'f-vacancylist-newnotfound'})
            if not new_jobs:
                table = soup.find('table',
                                  id='ctl00_content_vacancyList_gridList')
                if table:
                    tr_lst = table.find_all('tr', attrs={'id': True})
                    for tr in tr_lst:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('h2', attrs={'class': 'card-title'})
                            href = title.a['href']
                            content = div.find('div', attrs={'class': 'card-description'}).text
                            company = 'No name'
                            p = div.find('p', attrs={'class': 'company-name'})
                            if p:
                                company = p.a.text
                            jobs.append({
                                'title': title.text,
                                'url': domain + href,
                                'description': content,
                                'company': company})
                else:
                    errors.append({'url': url, 'title': "Table does not exists"})
            else:
                errors.append({'url': url, 'title': "Page is empty"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def dou(url):
    jobs = []
    errors = []
    # domain = 'https://jobs.dou.ua/'
    if url:
        resp = requests.get(url, headers=header[randint(0, 3)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_lst:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'sh-info'})
                    content = cont.text
                    company = 'No name'
                    a = title.find('a', attrs={'class': 'company'})
                    if a:
                        company = a.text
                    jobs.append({'title': title.text, 'url': href,
                                 'description': content, 'company': company})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def djinni(url):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    if url:
        resp = requests.get(url, headers=header[randint(0, 3)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')

            main_section = soup.find('section', attrs={'class': 'jobs-list-wrapper'})
            if main_section:
                article_lst = main_section.find_all('article')
                for article in article_lst:

                    title = article.find('p', attrs={'class': 'title'})
                    href = title.a['href']

                    company = 'No name'
                    comp = article.find('span', attrs={'class': 'company'})
                    if comp:
                        company = comp.text

                    discr = article.find_all('p', attrs={'class': 'svelte-rr20pa'})
                    for result in discr:
                        if len(result.attrs['class']) == 1:
                            content = result.text

                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company})

            else:
                errors.append({'url': url, 'title': "Section does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


if __name__ == '__main__':
    #url = 'https://djinni.co/jobs2/?category=python&location=kyiv&'
    #'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'
    url = 'https://jobs.dou.ua/vacancies/?city=Киев&category=Python'
    jobs, errors = dou(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    strr = ''
    for i in jobs:
        strr += str(i)
        strr += '\n'
    h.write(strr)
    h.close()
    h = codecs.open('errors.txt', 'w', 'utf-8')
    h.write(str(errors))
    h.close()

import asyncio
import codecs
import os
import sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

prg = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(prg)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django

django.setup()

from scraping.parser import *

from scraping.models import City, Language, Vacancy, Error, Url

# функция и ключ для url к ней
parser = (
    (work, 'work'),
    (rabota, 'rabota'),
    (djinni, 'djinni'),
    (dou, 'dou')
)
jobs, errors = [], []

User = get_user_model()

# возвращает список уникальных пар
def get_settings():
    qs = User.objects.filter(send_email=True).values()
    setting_list = set((q['city_id'], q['language_id']) for q in qs)
    return setting_list

# возвращает список url для уникальных пар settings
def get_urls(settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in settings:
        tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dct[pair]}
        urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)

# создаем асинхнонную петлю
loop = asyncio.get_event_loop()

#создаем список задач
tmp_task = [(func, data['url_data'][key], data['city'], data['language'])
            for data in url_list
            for func, key in parser]

#отправляем список на выполнение
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_task])

#for data in url_list:
#    for func, key in parser:
#        url = data['url_data'][key]
#        j, e = func(url, city=data['city'], language=data['language'])
#        jobs += j
#        errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors)
    try:
        er.save()
    except DatabaseError:
        pass


# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
#
# h = codecs.open('errors.txt', 'w', 'utf-8')
# h.write(str(errors))
# h.close()

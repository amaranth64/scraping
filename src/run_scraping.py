import codecs
import os
import sys

from django.db import DatabaseError

prg = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(prg)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django

django.setup()

from scraping.parser import *

from scraping.models import City, Language, Vacancy

parser = (
    (workSite, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (rabotaSite, 'https://rabota.ua/zapros/python/киев'),
    (djinni, 'https://djinni.co/jobs2/?category=python&location=kyiv&'),
    (dou, 'https://jobs.dou.ua/vacancies/?city=Киев&category=Python')
)

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []

for func, url in parser:
    j, e = func(url)
    jobs += j
    errors += e


for job in jobs:
    v = Vacancy(**job,city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()

h = codecs.open('errors.txt', 'w', 'utf-8')
h.write(str(errors))
h.close()

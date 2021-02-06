import datetime
import os
import sys
import django
from django.core.mail import EmailMultiAlternatives


from scraping_service.settings import EMAIL_HOST_USER

from django.contrib.auth import get_user_model
from django.db import DatabaseError


prg = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(prg)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'


django.setup()
from scraping.models import Vacancy,Error, Url
today = datetime.date.today()
print (today)
subject = f'Рассылка вакансий за {today}'
text_content = 'Рассылка вакансий'
from_email = EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER
User = get_user_model()
empty = '<h2>вакансий не найдено</h2>'

qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['email'])
if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows[:10]:
            html += f'<h5><a href="{ row["url"] }">{ row["title"] }</a></h5>'
            html += f'<p> { row["description"] } </p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            #msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            #msg.attach_alternative(_html, "text/html")
            #msg.send()

# отправка ошибок
qs = Error.objects.filter(timestamp=today)
to = ADMIN_USER
from_email = ADMIN_USER
subject = ''
text_content = ''

_html = ''
if qs.exists():
    error = qs.first()
    data = error.data['errors']
    for i in data:
        _html += f'<h5> <a href="{ i["url"] }"> Error: {i["title"]} </h5>'
    subject = f'ОШИБКИ СКРАППИНГА {today}'
    text_content = 'Ошибки'
    data = error.data['user_data']
    if data:
        _html += '<hr> <h2>Пожелания пользователей</h2>'
    for i in data:
        _html += f'<h5>Город: {i["city"]}, Cпециальность:{i["language"]}, Email:{i["email"]}</h5>'
    subject = f'Пожелания пользователей {today}'
    text_content = 'Пожелания пользователей'

qs = Url.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']):True for i in qs}
urls_err =''
for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0] and keys[1]:
            urls_err += f'<h5> для города {keys[0]} и ЯП {keys[1]} нет url </h5><br>'
if urls_err:
    subject += ' отсутствующие urls'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
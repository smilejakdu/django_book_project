import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

import django

django.setup()

from user.models import *
from blog.models import Book , Covid , Comment , Post


'''
item name
'''

item_bulk = []

with open('./covid.csv') as csv_file:
    data = csv.reader(csv_file)
    for row in data:
        item_bulk.append(Covid(area = row[1] , country = row[2] , patient = row[3] , dead = row[4]))

for i in range(1, len(item_bulk)):
    Covid.objects.filter(id=i).create(area    = item_bulk[i-1].area,
                                      country = item_bulk[i-1].country,
                                      patient = item_bulk[i-1].patient,
                                      dead    = item_bulk[i-1].dead,)


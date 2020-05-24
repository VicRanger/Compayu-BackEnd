import os
import sys
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE']='backsite.settings'
django.setup()

from compayu.models import Thought
from compayu.util import writeThought
f = open('./json/compayu_fixture.json')
text = f.readline()
res = eval(text)
for data in res:
    thought = {}
    thought['create-time'] = 
    break
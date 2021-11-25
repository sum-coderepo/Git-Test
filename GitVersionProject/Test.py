import sys
import os
import pathlib
import hashlib
import shutil
import time
import json

tracking_json = open('./.git/trackingArea.json', 'r')
res = {}
res = json.load(tracking_json)
print(type(res))
print(res)

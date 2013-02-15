#!/usr/bin/env python

from gspreadsheet import GSpreadsheet
import requests

import settings

sheet = GSpreadsheet(settings.SOURCE)

for row in sheet:
    print row
    url = row['url']
    if row['setup.pyurl'] is None:
        setup_url = url + '/blob/master/setup.py'
        response = requests.head(setup_url)
        row['setup.pyurl'] = setup_url if response.status_code == 200 else "missing"
    if row['setup.cfg'] is None:
        response = requests.head(url + '/blob/master/setup.cfg')
        row['setup.cfg'] = "1" if response.status_code == 200 else "0"
    if row['manifest.in'] is None:
        response = requests.head(url + '/blob/master/MANIFEST.in')
        row['manifest.in'] = "1" if response.status_code == 200 else "0"
    if row['makefile'] is None:
        response = requests.head(url + '/blob/master/Makefile')
        row['makefile'] = "1" if response.status_code == 200 else "0"
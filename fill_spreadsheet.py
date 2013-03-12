#!/usr/bin/env python

from gspreadsheet import GSpreadsheet
import requests

import settings

sheet = GSpreadsheet(settings.SOURCE)
print sheet.fieldnames

for row in sheet:
    print "* %s" % row['package']
    raw = None
    url = row['url']
    raw_url = 'https://raw.github.com/' + '/'.join(url.rsplit('/', 2)[1:]) + '/master/setup.py'
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
    if row['lines'] is None:
        if raw is None:
            raw = requests.get(raw_url)
        row['lines'] = str(raw.content.count('\n') + 1)
    if row['docstring'] is None:
        if raw is None:
            raw = requests.get(raw_url)
        docstring = []
        for i, line in enumerate(raw.content.splitlines()):
            if line.rstrip() == '"""':
                docstring.append(i)
        if docstring:
            row['docstring'] = str(docstring[1] - docstring[0] - 1)
        else:
            row['docstring'] = '-'

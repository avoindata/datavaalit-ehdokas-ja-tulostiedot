#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2013  Ville Korhonen

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import os
import sys
import argparse
import csv
import json
import datetime

_ = lambda x:x

def main(args):
    if not os.path.exists(args.infile):
        print "Input file %s not found." % args.infile
        return 1
    
    reader = csv.reader(open(args.infile, 'r'), delimiter=args.delimiter, quotechar=args.quotechar)

    data = []
    headers = None

    now = datetime.datetime.now()
    meta = {
        'source': {
            'url': 'http://pxweb2.stat.fi/database/StatFin/vaa/evaa/evaa_2011/150_evaa_tau_105_fi.csv',
            'sha256': '147785f360f2afcc6ffef37b9bf4dc2fe852e171a6fb4a75c14a3a3e691be8f1',
            'downloaded': '2013-09-26',
        },
        'created': now.strftime('%Y-%m%-d'),
        'author': 'Ville Korhonen <ville@xd.fi>',
        'description': 'Eduskuntavaalien 2011 ehdokaskohtainen äänisaalis ja vertailuluku. Luotu lataamalla lähdetiedosto, poistamalla ylimääräiset rivit (1, 3, 2319-), muutamalla ISO-8859-1 > UTF-8 ja suorittamalla CSV-JSON -muuntoskripti.',
        'fields': {
            'lastname': 'Ehdokkaan sukunimi',
            'firstname': 'Ehdokkaan etunimi',
            'party': 'Puolue',
            'area': 'Vaalipiiri',
            'votes': 'Äänimäärä',
            'vote_percentage': 'Ehdokkaan äänet prosenttia vaalipiirin kokonaismäärästä',
            'comp_number': 'Vertailuluku',
            'selected': 'Valittiinko henkilö eduskuntaan (kyllä/ei)',
        }
    }

    for row in reader:
        if headers is None:
            headers = row
            continue
        (person, party, area) = row[0].split('/')
        if person[0] == '*':
            person = person[1:]
            selected = True
        else:
            selected = False

        person = person.strip()
        (lastname, firstnames) = person.split(' ', 1)

        tmp = {
            #'name': person,
            'lastname': lastname,
            'firstname': firstnames,
            'party': party.strip(),
            'area': area.strip(),
            'votes': float(row[1]),
            'vote_percentage': float(row[2]),
            'comp_number': float(row[3]),
            'selected': selected,
        }
        data.append(tmp)
    structure = {
        'meta': meta,
        'data': data,
    }
    print json.dumps(structure)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', dest='infile')
    parser.add_argument('-d', '--delimiter', dest='delimiter', default=';')
    parser.add_argument('-c', '--quote-char', dest='quotechar', default='"')

    args = parser.parse_args()    
    sys.exit(main(args))

if __name__ == '__main__':
    run()

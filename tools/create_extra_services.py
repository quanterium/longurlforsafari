#!/usr/bin/env python

"""
A script to generate the JSON-formatted list of additional services not included
in the list on longurl.org. We use this rather than editing the JSON file directly
since its easier to maintain.
"""

import os

SERVICES = ['abcn.ws',
            'aje.me',
            'amzn.com',
            'aol.it',
            'apne.ws',
            'awe.sm',
            'bbc.in',
            'bcove.me',
            'blkatl.as',
            'bzfd.it',
            'cnt.to',
            'cog.gd',
            'coge.la',
            'cptl.st',
            'deadsp.in',
            'dft.ba'
            'digs.by',
            'dis.tl',
            'eicker.at',
            'engt.co',
            'es.pn',
            'ex-c.it',
            'exm.nr',
            'fk.cm',
            'frypi.cc',
            'fxn.ws',
            'fyad.org',
            'fyre.it',
            'gr.pn',
            'grpn.eu',
            'gu.com',
            'hawna.ir',
            'hnl.me',
            'inv.lv',
            'itun.es',
            'journ.us',
            'kpbs.us',
            'lifehac.kr',
            'me.lt',
            'mmflint.me',
            'on.mash.to',
            'on.msnbc.com',
            'on.natgeo.com',
            'on.wsj.com',
            'oft.me',
            'p2.to',
            'path.to',
            'pep.si',
            'pitch.pe',
            'qr.ae',
            'reg.cx',
            'reut.rs',
            'rww.to',
            'ry.ly',
            's.meulie.net',
            'scr.bi',
            'selnd.com',
            'shorten.ws',
            'shr.gd'
            'slate.me',
            'socuteurl.com',
            'spn.tw',
            'spr.ly',
            'ti.me',
            'to.pbs.org',
            'un.cr',
            'url4t.com',
            'veh.cl',
            'wrd.tw'
           ]

OUTPUT_FILE = os.path.abspath(os.path.join('..', 'release', 'extra_services.json.txt'))

str = '{'
for service in SERVICES:
  str += '"%s":{"domain":"%s","regex":""},' % (service, service)
str = str[:-1] + '}'
out = open(OUTPUT_FILE, 'w')
out.write(str)
out.close()

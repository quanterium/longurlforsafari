#!/usr/bin/env python

"""
A script to generate the JSON-formatted list of additional services not included
in the list on longurl.org. We use this rather than editing the JSON file directly
since its easier to maintain.

Copyright (c) 2011, David Mueller
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the names of the the developers nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL DAVID MUELLER NOR TITI BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os

SERVICES = ['1.usa.gov',
            'abcn.ws',
            'aexp.co',
            'aje.me',
            'amzn.com',
            'ana.ms',
            'aol.it',
            'apne.ws',
            'atmlb.com',
            'avc.lu',
            'avwk.us',
            'awe.sm',
            'bbc.in',
            'bcove.me',
            'blkatl.as',
            'bloom.bg',
            'bo.st',
            'buswk.co',
            'bzfd.it',
            'clic.gs',
            'clrlv.rs',
            'cnet.co',
            'cnt.to',
            'cog.gd',
            'coge.la',
            'cptl.st',
            'db.tt',
            'deadsp.in',
            'dft.ba',
            'dhurl.org',
            'digs.by',
            'dis.tl',
            'eicker.at',
            'engt.co',
            'eonli.ne',
            'ericri.es',
            'es.pn',
            'ex-c.it',
            'exci.to',
            'exm.nr',
            'fandan.co',
            'fk.cm',
            'frypi.cc',
            'fxn.ws',
            'fyad.org',
            'fyre.it',
            'go.nasa.gov',
            'go-att.us',
            'gofly.us',
            'gr.pn',
            'grpn.eu',
            'gu.com',
            'hawna.ir',
            'hnl.me',
            'ht.ly',
            'icont.ac',
            'inv.lv',
            'itsh.bo',
            'itun.es',
            'journ.us',
            'kpbs.us',
            'lifehac.kr',
            'lil.as',
            'lsnlw.com',
            'mbist.ro',
            'me.lt',
            'mm4a.org',
            'mmflint.me',
            'nerdi.st',
            'newwp.it',
            'ning.it',
            'nmsk.co',
            'nyr.kr',
            'ofa.bo',
            'on.doi.gov',
            'on.kayak.com',
            'on.mash.to',
            'on.msnbc.com',
            'on.natgeo.com',
            'on.wsj.com',
            'on-msn.com',
            'onforb.es',
            'p2.to',
            'path.to',
            'pep.si',
            'ping.fm',
            'pitch.pe',
            'prn.to',
            'pulsene.ws',
            'qr.ae',
            'red.ht',
            'redd.it',
            'reg.cx',
            'reut.rs',
            'rww.to',
            'ry.ly',
            's.meulie.net',
            'sbne.ws',
            'sch.mp',
            'scr.bi',
            'seati.ms',
            'selnd.com',
            'sfg.ly',
            'shorten.ws',
            'slate.me',
            'sns.ly',
            'socuteurl.com',
            'spn.tw',
            'spr.ly',
            'svy.mk',
            'theatln.tc',
            'thesent.nl',
            'ti.me',
            'to.pbs.org',
            'tox.cx',
            'tvly.com',
            'tw.itunes.com',
            'twe.ly',
            'u.bzz.com',
            'un.cr',
            'urbns.pn',
            'url4t.com',
            'veh.cl',
            'vosd.org',
            'wrd.tw',
            'yowz.at',
            'zite.to'
           ]

OUTPUT_FILE = os.path.abspath(os.path.join('..', 'release', 'extra_services.json.txt'))

str = '{'
for service in SERVICES:
  str += '"%s":{"domain":"%s","regex":""},' % (service, service)
str = str[:-1] + '}'
out = open(OUTPUT_FILE, 'w')
out.write(str)
out.close()

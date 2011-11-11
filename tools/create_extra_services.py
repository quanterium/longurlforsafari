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
            '1click.at',
            '4fun.tw',
            'aarp.us',
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
            'b-gat.es',
            'b0x.ee',
            'bbc.in',
            'bcove.me',
            'bddy.me',
            'blkatl.as',
            'bloom.bg',
            'bo.st',
            'buswk.co',
            'bzfd.it',
            'chn.ge',
            'clic.gs',
            'clrlv.rs',
            'cnet.co',
            'cnt.to',
            'cog.gd',
            'coge.la',
            'cour.at',
            'cptl.st',
            'db.tt',
            'deadsp.in',
            'dft.ba',
            'dhurl.org',
            'di.sn',
            'digs.by',
            'dis.tl',
            'dthin.gs',
            'econ.st',
            'eicker.at',
            'engt.co',
            'eonli.ne',
            'epho.st',
            'epi.us',
            'ericri.es',
            'es.pn',
            'ex-c.it',
            'exci.to',
            'exm.nr',
            'fandan.co',
            'fk.cm',
            'flpbd.it',
            'frypi.cc',
            'fxn.ws',
            'fyad.org',
            'fyre.it',
            'gi.lt',
            'global-en.co',
            'go.nasa.gov',
            'go-att.us',
            'gofly.us',
            'gogo.to',
            'gplus.to',
            'gqm.ag',
            'gr.pn',
            'grpn.eu',
            'gtcha.me',
            'gu.com',
            'hawna.ir',
            'hip.mu',
            'hnl.me',
            'ht.ly',
            'icont.ac',
            'inv.lv',
            'itsh.bo',
            'itun.es',
            'journ.us',
            'krz.ch',
            'kpbs.us',
            'l.pr',
            'lifehac.kr',
            'lil.as',
            'lnk.nu',
            'lsnlw.com',
            'macw.us',
            'mbist.ro',
            'mcaf.ee',
            'mcch.at',
            'me.lt',
            'meme.ms',
            'mil-com.me',
            'mktplc.org',
            'mm4a.org',
            'mmflint.me',
            'movi.ps',
            'mykl.co',
            'n9n.us',
            'nctim.es',
            'nerdi.st',
            'newwp.it',
            'ning.it',
            'nmsk.co',
            'nydn.us',
            'nyr.kr',
            'ofa.bo',
            'on.cc.com',
            'on.cclol.com',
            'on.doi.gov',
            'on.ft.com',
            'on.kayak.com',
            'on.mash.to',
            'on.msnbc.com',
            'on.natgeo.com',
            'on.wsj.com',
            'on-msn.com',
            'onforb.es',
            'owl.li',
            'p2.to',
            'path.to',
            'pep.si',
            'ping.fm',
            'pitch.pe',
            'prn.to',
            'pulp.ly',
            'pulsene.ws',
            'qr.ae',
            'qurl.com',
            'rca.st',
            're.pn',
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
            'sgp.cm',
            'shorten.ws',
            'skygrid.me',
            'slate.me',
            'smarturl.it',
            'smf.is',
            'sns.mx',
            'sns.ly',
            'soc.li',
            'socuteurl.com',
            'spn.tw',
            'spr.ly',
            'srtu.in',
            'stk.ly',
            'svy.mk',
            'tgr.ph',
            'theatln.tc',
            'thesent.nl',
            'thkpr.gs',
            'ti.me',
            'tnw.co',
            'tnw.to',
            'to.pbs.org',
            'tox.cx',
            'tvly.com',
            'tw.itunes.com',
            'twe.ly',
            'twitlink.ws',
            'u.bzz.com',
            'un.cr',
            'urbns.pn',
            'url4t.com',
            'veh.cl',
            'virg.co',
            'vosd.org',
            'wandr.me',
            'wcti.us',
            'wpo.st',
            'wrd.tw',
            'x2q.us',
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

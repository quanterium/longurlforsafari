#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to generate the JSON-formatted list of services supported by the
extension. We use this rather than editing the JSON file directly
since its easier to maintain.

It's called create_extra_services since originally this list was just
additional extensions that worked but weren't included in the list obtained
from LongURL.org, but since the extension was reworked to function on its
own, this list is now all the services, not just "extra" ones.

Copyright (c) 2011-2016, David Mueller
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

SERVICES = ['›.ws',
            '✩.ws',
            '✿.ws',
            '❥.ws',
            '➔.ws',
            '➞.ws',
            '➡.ws',
            '➨.ws',
            '➯.ws',
            '➹.ws',
            '➽.ws',
            '0rz.tw',
            '1.usa.gov',
            '1click.at',
            '1link.in',
            '1url.com',
            '2.gp',
            '2big.at',
            '2tu.us',
            '3.ly',
            '307.to',
            '4fun.tw',
            '4ms.me',
            '4sq.com',
            '4url.cc',
            '6url.com',
            '7.ly',
            '7ny.tv',
            'a.gg',
            'a.nf',
            'aa.cx',
            'aarp.us',
            'abcn.ws',
            'abcurl.net',
            'ad.vu',
            'adf.ly',
            'adjix.com',
            'aexp.co',
            'afx.cc',
            'aje.me',
            'all.fuseurl.com',
            'alturl.com',
            'amzn.com',
            'amzn.to',
            'ana.ms',
            'aol.it',
            'apne.ws',
            'ar.gy',
            'arst.ch',
            'atmlb.com',
            'atu.ca',
            'avc.lu',
            'avwk.us',
            'awe.sm',
            'azc.cc',
            'b-gat.es',
            'b.qr.ae',
            'b0x.ee',
            'b23.ru',
            'b2l.me',
            'bacn.me',
            'bbc.in',
            'bcool.bz',
            'bcove.me',
            'bddy.me',
            'binged.it',
            'bit.ly',
            'bizj.us',
            'blkatl.as',
            'bloat.me',
            'bloom.bg',
            'bo.st',
            'bravo.ly',
            'bsa.ly',
            'budurl.com',
            'buff.ly',
            'buswk.co',
            'bzfd.it',
            'canurl.com',
            'chilp.it',
            'chn.ge',
            'chzb.gr',
            'cl.lk',
            'cl.ly',
            'clck.ru',
            'cli.gs',
            'clic.gs',
            'cliccami.info',
            'clickthru.ca',
            'clop.in',
            'clrlv.rs',
            'cnet.co',
            'cnt.to',
            'cog.gd',
            'coge.la',
            'conta.cc',
            'cort.as',
            'cot.ag',
            'cour.at',
            'cptl.st',
            'crks.me',
            'csc0.ly',
            'ctvr.us',
            'cutt.us',
            'dai.ly',
            'db.tt',
            'deadsp.in',
            'decenturl.com',
            'dfl8.me',
            'dft.ba',
            'dhurl.org',
            'di.sn',
            'digbig.com',
            'digg.com',
            'digs.by',
            'dis.tl',
            'disq.us',
            'dld.bz',
            'dlvr.it',
            'do.my',
            'doiop.com',
            'dopen.us',
            'dthin.gs',
            'easyuri.com',
            'easyurl.net',
            'econ.st',
            'eepurl.com',
            'eicker.at',
            'engt.co',
            'eonli.ne',
            'epho.st',
            'epi.us',
            'ericri.es',
            'es.pn',
            'eweri.com',
            'ex-c.it',
            'exci.to',
            'exm.nr',
            'fa.by',
            'fandan.co',
            'fav.me',
            'fb.me',
            'fbshare.me',
            'ff.im',
            'fff.to',
            'fire.to',
            'firsturl.de',
            'firsturl.net',
            'fk.cm',
            'flic.kr',
            'flpbd.it',
            'flq.us',
            'fly2.ws',
            'fon.gs',
            'freak.to',
            'frypi.cc',
            'fuseurl.com',
            'fuzzy.to',
            'fwd4.me',
            'fwib.net',
            'fxn.ws',
            'fyad.org',
            'fyre.it',
            'g.co',
            'g.ro.lt',
            'gi.lt',
            'gizmo.do',
            'gl.am',
            'global-en.co',
            'go-att.us',
            'go.9nl.com',
            'go.fly.com',
            'go.nasa.gov',
            'go.usa.gov',
            'gofly.us',
            'gogo.to',
            'goo.gl',
            'goshrink.com',
            'gplus.to',
            'gqm.ag',
            'gr.pn',
            'grpn.eu',
            'gtcha.me',
            'gtnr.it',
            'gu.com',
            'gurl.es',
            'hawna.ir',
            'hex.io',
            'hiderefer.com',
            'hip.mu',
            'hive.rs',
            'hmm.ph',
            'hnl.me',
            'href.in',
            'hsblinks.com',
            'ht.ly',
            'htxt.it',
            'huff.to',
            'hulu.com',
            'hurl.me',
            'hurl.ws',
            'icanhaz.com',
            'icont.ac',
            'idek.net',
            'ilix.in',
            'inv.lv',
            'is.gd',
            'its.my',
            'itsh.bo',
            'itun.es',
            'iuo8.tk',
            'ix.lt',
            'j.mp',
            'jijr.com',
            'journ.us',
            'kiro.tv',
            'kl.am',
            'klck.me',
            'korta.nu',
            'kpbs.us',
            'krunchd.com',
            'krz.ch',
            'l.pr',
            'l9k.net',
            'lat.ms',
            'lifehac.kr',
            'liip.to',
            'lil.as',
            'liltext.com',
            'linkbee.com',
            'linkbun.ch',
            'liurl.cn',
            'ln-s.net',
            'ln-s.ru',
            'lnk.gd',
            'lnk.ms',
            'lnk.nu',
            'lnkd.in',
            'lnkurl.com',
            'lru.jp',
            'lsnlw.com',
            'lt.tl',
            'lurl.no',
            'macte.ch',
            'macw.us',
            'mash.to',
            'mbist.ro',
            'mcaf.ee',
            'mcch.at',
            'me.lt',
            'meme.ms',
            'merky.de',
            'migre.me',
            'mil-com.me',
            'miniurl.com',
            'minurl.fr',
            'mke.me',
            'mktplc.org',
            'mm4a.org',
            'mmflint.me',
            'moby.to',
            'moourl.com',
            'movi.ps',
            'mrte.ch',
            'mykl.co',
            'myloc.me',
            'myurl.in',
            'n.pr',
            'n9n.us',
            'nbc.co',
            'nblo.gs',
            'nctim.es',
            'nerdi.st',
            'newwp.it',
            'ning.it',
            'nmsk.co',
            'nn.nf',
            'not.my',
            'notlong.com',
            'nsfw.in',
            'nutshellurl.com',
            'nxy.in',
            'nydn.us',
            'nyr.kr',
            'nyti.ms',
            'o-x.fr',
            'oc1.us',
            'ofa.bo',
            'om.ly',
            'omf.gd',
            'omoikane.net',
            'on-msn.com',
            'on.cc.com',
            'on.cclol.com',
            'on.cnn.com',
            'on.doi.gov',
            'on.ft.com',
            'on.hwnair.com',
            'on.kayak.com',
            'on.mash.to',
            'on.mktw.net',
            'on.msnbc.com',
            'on.natgeo.com',
            'on.wsj.com',
            'onforb.es',
            'orz.se',
            'ow.ly',
            'owl.li',
            'p2.to',
            'path.to',
            'pep.si',
            'ping.fm',
            'pitch.pe',
            'pli.gs',
            'pnt.me',
            'politi.co',
            'post.ly',
            'pp.gg',
            'prn.to',
            'profile.to',
            'ptiturl.com',
            'pub.vitrue.com',
            'pulp.ly',
            'pulsene.ws',
            'qlnk.net',
            'qr.ae',
            'qte.me',
            'qu.tc',
            'qurl.com',
            'r.im',
            'rb6.me',
            'rca.st',
            're.pn',
            'read.bi',
            'readthis.ca',
            'reallytinyurl.com',
            'red.ht',
            'redd.it',
            'redir.ec',
            'redirects.ca',
            'redirx.com',
            'reg.cx',
            'retwt.me',
            'reut.rs',
            'ri.ms',
            'rickroll.it',
            'riz.gd',
            'rt.nu',
            'ru.ly',
            'rubyurl.com',
            'rurl.org',
            'rww.to',
            'rww.tw',
            'ry.ly',
            's.meulie.net',
            's4c.in',
            's7y.us',
            'safe.mn',
            'sbne.ws',
            'sch.mp',
            'scr.bi',
            'sdut.us',
            'seati.ms',
            'see.sc',
            'selnd.com',
            'sfg.ly',
            'sgp.cm',
            'shar.es',
            'shink.de',
            'shorl.com',
            'short.ie',
            'short.to',
            'shorten.ws',
            'shortlinks.co.uk',
            'shorturl.com',
            'shout.to',
            'show.my',
            'shrinkify.com',
            'shrinkr.com',
            'shrt.fr',
            'shrt.st',
            'shrten.com',
            'shrunkin.com',
            'simurl.com',
            'skygrid.me',
            'slate.me',
            'smallr.com',
            'smarturl.it',
            'smf.is',
            'smsh.me',
            'smurl.name',
            'sn.im',
            'snipr.com',
            'snipurl.com',
            'sns.ly',
            'sns.mx',
            'snurl.com',
            'soc.li',
            'socuteurl.com',
            'sp2.ro',
            'spedr.com',
            'spn.tw',
            'spr.ly',
            'srnk.net',
            'srs.li',
            'srtu.in',
            'starturl.com',
            'stk.ly',
            'su.pr',
            'surl.co.uk',
            'surl.hu',
            'svy.mk',
            't.co',
            't.lh.com',
            'ta.gd',
            'tbd.ly',
            'tcrn.ch',
            'tgo.co',
            'tgr.me',
            'tgr.ph',
            'theatln.tc',
            'thesent.nl',
            'thkpr.gs',
            'ti.me',
            'tighturl.com',
            'tiniuri.com',
            'tiny.cc',
            'tiny.ly',
            'tiny.pl',
            'tinylink.in',
            'tinyuri.ca',
            'tinyurl.com',
            'tk.',
            'tl.gd',
            'tmi.me',
            'tnij.org',
            'tnw.co',
            'tnw.to',
            'tny.com',
            'to.',
            'to.ly',
            'to.pbs.org',
            'togoto.us',
            'totc.us',
            'tox.cx',
            'toysr.us',
            'tpm.ly',
            'tr.im',
            'tra.kz',
            'tripadv.sr',
            'trunc.it',
            'tvly.com',
            'tw.itunes.com',
            'twe.ly',
            'twhub.com',
            'twirl.at',
            'twitclicks.com',
            'twitlink.ws',
            'twitterurl.net',
            'twitterurl.org',
            'twiturl.de',
            'twurl.cc',
            'twurl.nl',
            'u.bzz.com',
            'u.mavrev.com',
            'u.nu',
            'u76.org',
            'ub0.cc',
            'ulu.lu',
            'un.cr',
            'updating.me',
            'ur1.ca',
            'urbns.pn',
            'url.az',
            'url.co.uk',
            'url.ie',
            'url360.me',
            'url4.eu',
            'url4t.com',
            'urlborg.com',
            'urlbrief.com',
            'urlcover.com',
            'urlcut.com',
            'urlenco.de',
            'urli.nl',
            'urls.im',
            'urlshorteningservicefortwitter.com',
            'urlx.ie',
            'urlzen.com',
            'usat.ly',
            'use.my',
            'v.iew.im',
            'vb.ly',
            'veh.cl',
            'vgn.am',
            'virg.co',
            'vl.am',
            'vosd.org',
            'vwoa.us',
            'w.ly',
            'w55.de',
            'wandr.me',
            'wapo.st',
            'wapurl.co.uk',
            'wcti.us',
            'wipi.es',
            'wp.me',
            'wpo.st',
            'wrd.tw',
            'wxch.nl',
            'x.vu',
            'x2q.us',
            'xr.com',
            'xrl.in',
            'xrl.us',
            'xurl.es',
            'xurl.jp',
            'y.ahoo.it',
            'yatuc.com',
            'ye.pe',
            'yep.it',
            'yfrog.com',
            'yhoo.it',
            'yiyd.com',
            'youtu.be',
            'yowz.at',
            'yuarel.com',
            'z0p.de',
            'zi.ma',
            'zi.mu',
            'zipmyurl.com',
            'zite.to',
            'zud.me',
            'zurl.ws',
            'zz.gd',
            'zzang.kr'
           ]

OUTPUT_FILE = os.path.abspath(os.path.join('..', 'release', 'extra_services.json.txt'))
WIKI_FILE = os.path.abspath(os.path.join('..', '..', 'longurlforsafari.wiki', 'Shortening-Services.md'))

wiki_str = '''# Introduction

To avoid having to check every link on a page, the extension retrieves a list of known domains of URL shortening services. This list is retrieved each time Safari is started, allowing the list to be updated without requiring a new version of the extension to be created.

If you come across a domain being used for short URLs that isn't on this list, openen an issue in [the issue tracker](https://github.com/quanterium/longurlforsafari/issues) is the easiest way to have the domain added.

# Supported Domains
'''
output_str = '{'
for service in SERVICES:
  output_str += '"%s":{"domain":"%s","regex":""},' % (service, service)
  wiki_str += ' * %s\n' % service
output_str = output_str[:-1] + '}'
out = open(OUTPUT_FILE, 'w')
out.write(output_str)
out.close()
out = open(WIKI_FILE, 'w')
out.write(wiki_str)
out.close()

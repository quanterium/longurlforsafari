#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to extract the list of vanity url shorteners maintained at
vanityurlshorteners.com and add them to the list in create_extra_services.py.

This script doesn't actually update create_extra_services.py, it instead
outputs an updated SERVICES list that can be copy and pasted into
create_extra_services.py.

Copyright (c) 2017, David Mueller
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
import sys
import time
import urllib
from HTMLParser import HTMLParser

import create_extra_services

class MyHTMLParser(HTMLParser):
  """
  This is our custom HTML parser class. We don't care about the full page, we just want the
  vanity domains. The stuff we care about is in a div tag with class 'content-holder'. In that
  div is a table with two columns, the second column is the one with the domain.
  """
  def __init__(self, services):
    HTMLParser.__init__(self)
    self.services = services
    self.in_content_holder = False
    self.in_tbody = False
    self.td_count = 0
    self.parsed_something = False
  
  def handle_starttag(self, tag, attrs):
    if tag == 'div':
      for attr in attrs:
        if attr[0] == 'class' and attr[1] == 'content-holder':
          self.in_content_holder = True
          return
    if not self.in_content_holder:
      return
    if tag == 'tbody':
      self.in_tbody = True
      return
    if not self.in_tbody:
      return
    if tag == 'tr':
      self.td_count = 0
      return
    if tag == 'td':
      self.td_count += 1
      return

  def handle_endtag(self, tag):
    if tag == 'tbody':
      self.in_tbody = False
    elif tag == 'div':
      self.in_content_holder = False

  def handle_data(self, data):
    if self.in_content_holder and self.in_tbody and self.td_count == 2:
      service = data.strip()
      if len(service) > 0:
        contents = service.split()
        for content in contents:
          if '.' in content:
            self.services.add(content)
            self.parsed_something = True

def get_page_content(url):
  page = urllib.urlopen(url)
  headers = page.info()
  page_len = headers.getheader('Content-Length')
  content = page.read(page_len)
  page.close()
  return content

def parse_page(url, content, services):
  parser = MyHTMLParser(services)
  parser.feed(content)
  if not parser.parsed_something:
    sys.stderr.write('WARNING: Failed to parse content from %s %s' % (url, os.linesep))
  return parser.services

if __name__ == '__main__':
  services_set = set(create_extra_services.SERVICES)
  for letter in xrange(ord('a'), ord('z')+1):
    url = 'http://www.vanityurlshorteners.com/%s' % chr(letter)
    content = get_page_content(url)
    services_set = parse_page(url, content, services_set)
    time.sleep(2)
  services_list = list(services_set)
  services_list.sort()
  print 'SERVICES = ['
  for service in services_list:
    print "            '%s'," % service
  print '           ]'

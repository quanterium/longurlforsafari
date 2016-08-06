/*
Copyright (c) 2010-2016, David Mueller, TiTi
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

Based on the "LongURL" Google Chrome extension, version 1.7 developed by TiTi,
released undeer the WTFPL license.
https://chrome.google.com/extensions/detail/oldnehmjgfcannmkgkojafngdkhfkdpd
*/

// define an object constructor to hold the results
function ResultObject()
{
  this.metaDescription = false;
  this.metaKeywords = false;
  this.allRedirects = [];
  this.contentType = false;
  this.relCanonical = false;
  this.longUrl = false;
  this.title = false;
  this.responseCode = 200;
}

var LongURL = 
{
  options:
  {
    showPopup: true, // Show a tooltip when the mouse is over the link
    replaceHref: true, // For security and rapidity, true is more than recommended ; Replace the link your browser will hit if you click the link
    replaceVisibleHref: 0, // 0: no, 1: title, 2: link ; default=1 as recommended by W3C : http://www.w3.org/TR/WCAG10-HTML-TECHS/#link-text ; http://www.w3.org/TR/WCAG20-HTML-TECHS/
    forceVisibleHref: false, // Force change of the link text even if it's not the target - Example: <a href="http://is.gd/w">Home page of Google</a>
    autoExpand: true, // Automatically expand short URLs
    logHeader: '[LongURL]',
    
    // Tooltip content options
    showAllRedirects: 0,
    showContentType: 0,
    showTitle: 1,
    showRelCanonical: 0,
    showMetaKeywords: 0,
    showMetaDescription: 0,
    showShortUrl: 1
  },
  
  callbacks: [], // The global callbacks array that stores a reference to all active callbacks
  
  preparedRequests: 0, // Total number of requests to LongURL API
  
  storedRequests: {},
  
  known_services: {},
  
  // Call LongURL webservice and define callback
  prepareRequest: function(msgEvent)
  {
    var link = msgEvent.message;
    if(LongURL.storedRequests[link])
    {
      // This tinyurl has already been listed, maybe in another page, stop here!
      
      var json = LongURL.storedRequests[link];
      console.log(LongURL.options.logHeader + ' [Cache] Send ' + link + ' -> ' + json['longUrl']);
      msgEvent.target.page.dispatchMessage('lookupResult', {'link': link, 'json':json}); // Send data to content script
      return;
    }
    
    LongURL.storedRequests[link] = null; // Init
    
    // We create `i` - the current position - so that it will be available to the closure
    var i = LongURL.callbacks.length;
    
    // Now add our custom callback to the callback array so that the added script node can access it
    LongURL.callbacks[i] = function(json)
    {
      // Store the data
      LongURL.storedRequests[link] = json;
      
      // Anaylze result
      LongURL.processRequest(msgEvent);
      
      // Clear out our entry in the callback array since we don't need it anymore
      LongURL.callbacks[i] = null;
      delete LongURL.callbacks[i];
      
      // Clear out all outer variables referenced in the closure to prevent memory leaks in some browsers (Opera & FF not concerned?)
      i = null;
    };
    
    // Get the URL to find out where it redirects
    var resultObject = new ResultObject();
    LongURL.followURL(link, resultObject, i);
    
    LongURL.preparedRequests++;
  },
  
  // Analyze LongURL result and send data to content script
  processRequest: function(msgEvent)
  {
    try
    {
      var link = msgEvent.message;
      var json = LongURL.storedRequests[link];
      
      if(json['responseCode'] != 200) // Will never get into the if with LongURL API 2.0?
      {
        if(json['messages'])
        {
          for(var j = 0; j < json['messages'].length; j++)
          {
            throw('Server Response - ' + json['messages'][j]['type'] + ': ' + json['messages'][j]['message'] + ' For ' + link);
          }
        }
        else
        {
          throw('Server Response Error ' + json['responseCode'] + ', for ' + link);
        }
      }
      else
      {
        console.log(LongURL.options.logHeader + '[Fresh] Got ' + link + ' -> ' + json['longUrl']);
        msgEvent.target.page.dispatchMessage('lookupResult', {'link': link, 'json':json}); // Send data to content script
      }
    }
    catch(err)
    {
      console.log(LongURL.options.logHeader + ' [ERROR] ' + err);
    }
  },
  
  // Follow a link to find out the destination
  followURL: function(link, resultObject, i)
  {
    resultObject.allRedirects.push(link);
    resultObject.longUrl = link;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(data)
    {
      if(xhr.readyState == 4)
      {
        switch_block:
        {
          switch(xhr.status)
          {
            case 200:
              // XMLHttpRequest automatically follows redirects so we'll actually always wind up
              // here, but we'll leave the other cases in case we find another way to do this
              // See http://stackoverflow.com/questions/228225/prevent-redirection-of-xmlhttprequest
              var metas = xhr.response.getElementsByTagName('meta'); 
              for (var z=0; z<metas.length; z++)
              {
                if (metas[z].getAttribute('http-equiv') == 'refresh')
                {
                  // Got a meta http-equiv refresh tag
                  var content = metas[z].getAttribute('content').split(';');
                  if (content[0] == '0' && content[1].substring(0, 4).toUpperCase() == 'URL=')
                  {
                    var new_link = content[1].substring(4);
                    if (new_link != resultObject.longUrl)
                    {
                      LongURL.followURL(new_link, resultObject, i);
                      break switch_block;
                    }
                  }
                }
              }
              resultObject.longUrl = xhr.responseURL;
              pageData = LongURL.gatherPageData(xhr, resultObject);
              LongURL.callbacks[i](pageData);
              break;
            case 301:
            case 302:
            case 303:
            case 307:
            case 308:
              // Got a redirect
              var new_link = xhr.getResponseHeader('Location');
              if (new_link == null)
              {
                // Got a redirect without a location header, so we'll treat this like a 200
                pageData = LongURL.gatherPageData(xhr, resultObject);
                LongURL.callbacks[i](pageData);
              }
              else
              {
                LongURL.followURL(new_link, resultObject, i);
              }
              break;
            default:
              // Got something else we're not sure how to handle
              console.log(LongURL.options.logHeader + ' [ERROR] xhr.status='+xhr.status);
              break;
          }
        }
      }
    }
    xhr.responseType = "document";
    xhr.open('GET', link, true);
    xhr.send();
  },
  
  // Gather the page data into an object to use later
  gatherPageData: function(xhr, resultObject)
  {
    if (LongURL.options.showAllRedirects == 0)
    {
      resultObject.allRedirects = false;
    }
    if (LongURL.options.showContentType == 1)
    {
      resultObject.contentType = xhr.getResponseHeader('Content-Type');
    }
    if (xhr.response != null)
    {
      if (LongURL.options.showTitle == 1)
      {
        var title = xhr.response.getElementsByTagName("title");
        if (title.length > 0)
        {
          resultObject.title = title[0].innerHTML;
        }
      }
      var metas = xhr.response.getElementsByTagName('meta'); 
      for (var z=0; z<metas.length; z++)
      {
        if (LongURL.options.showMetaDescription == 1 && metas[z].getAttribute('name') == 'description')
        {
           resultObject.metaDescription = metas[z].getAttribute('content');
        }
        if (LongURL.options.showMetaKeywords == 1 && metas[z].getAttribute('name') == 'keywords')
        {
           resultObject.metaKeywords = metas[z].getAttribute('content');
        }
      }
      var links = xhr.response.getElementsByTagName('link'); 
      for (var z=0; z<links.length; z++)
      {
        if (LongURL.options.showRelCanonical == 1 && links[z].getAttribute('rel') == 'canonical')
        {
           resultObject.relCanonical = links[z].getAttribute('href');
        }
      }
    }
    return resultObject;
  }
};

// Escapes special characters with backslashes.
function escape(text) {
	if (!arguments.callee.escapeRE) {
		var specials = [ ".", "*", "+", "?", "|", "(", ")", "[", "]", "{", "}", "\\" ];
		arguments.callee.escapeRE = new RegExp( "(\\" + specials.join("|\\") + ")", "g" );
	}
	return text.replace(arguments.callee.escapeRE, "\\$1");
}

// Rebuild the blacklist from the settings. This is triggered automatically the first
// time the script runs, and via a listener when the user modifies the settings.
function rebuildBlacklist() {
	var str = safari.extension.settings.getItem("blacklist");
	var sites = str.split(/ *, */);
	
	document.blacklistRE = sites;
}

// Cache the RegExp object in this document for speed.
function getBlacklistRE() {
	if (!document.blacklistRE) {
		rebuildBlacklist();
	}
	return document.blacklistRE;
}

// Returns true if the URL is allowed to load.
function allowedToLoad(msgEvent) {
  var blacklistRE = getBlacklistRE();
  if (blacklistRE.indexOf(msgEvent.message) != -1) {
    msgEvent.target.page.dispatchMessage('blacklistResult', 'block');
  }
  else
  {
    msgEvent.target.page.dispatchMessage('blacklistResult', 'allow');
  }
}


//----------
// Get options from settings in Safari preferences window
function readSettings(msgEvent)
{
  LongURL.options.showPopup = safari.extension.settings.getItem('showPopup');
  LongURL.options.replaceHref = safari.extension.settings.getItem('replaceHref');
  LongURL.options.replaceVisibleHref = safari.extension.settings.getItem('replaceVisibleHref');
  LongURL.options.forceVisibleHref = safari.extension.settings.getItem('forceVisibleHref');
  LongURL.options.showAllRedirects = safari.extension.settings.getItem('showAllRedirects');
  LongURL.options.showContentType = safari.extension.settings.getItem('showContentType');
  LongURL.options.showTitle = safari.extension.settings.getItem('showTitle');
  LongURL.options.showRelCanonical = safari.extension.settings.getItem('showRelCanonical');
  LongURL.options.showMetaKeywords = safari.extension.settings.getItem('showMetaKeywords');
  LongURL.options.showMetaDescription = safari.extension.settings.getItem('showMetaDescription');
  LongURL.options.showShortUrl = safari.extension.settings.getItem('showShortUrl');
  LongURL.options.autoExpand = safari.extension.settings.getItem('autoExpand');
  if (msgEvent != null)
  {
    if ((msgEvent.key == 'showAllRedirects') || (msgEvent.key == 'showContentType') || (msgEvent.key == 'showTitle') || (msgEvent.key == 'showRelCananical') || (msgEvent.key == 'showMetaKeywords') || (msgEvent.key == 'showMetaDescription'))
    {
      // User changed contents to the tooltip, so flush the cache
      console.log(LongURL.options.logHeader + ' [Cache] Flushed due to tooltip contents change');
      LongURL.storedRequests = {};
    }
  }
  rebuildBlacklist();
}


// Get the list of supported services from LongURL
function requestServices()
{
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(data)
  {
    if(xhr.readyState == 4)
    {
      if(xhr.status == 200)
      {  
        LongURL.known_services = JSON.parse(xhr.responseText);
        console.log(LongURL.options.logHeader + ' [INFO] Loaded services list');
      }
      else
      {
        console.log(LongURL.options.logHeader + ' [ERROR] Failed to retrieve services list; xhr.status='+xhr.status);
      }
    }
  }
  xhr.open('GET', 'https://raw.githubusercontent.com/quanterium/longurlforsafari/master/release/extra_services.json.txt', true);
  xhr.send();
}

//----------

/**
* Handles data sent via safari.self.tab.dispatchMessage().
*/
function onRequest(msgEvent)
{
  // message is a request to do a LongURL lookup
  if (msgEvent.name === 'getLink')
  {
    LongURL.prepareRequest(msgEvent);
  }
  // message is a blacklist check
  else if (msgEvent.name === 'checkBlacklist')
  {
    allowedToLoad(msgEvent);
  }
  // message is a request for the configuration options
  else if (msgEvent.name === 'getOptions')
  {
    msgEvent.target.page.dispatchMessage('setOptions', LongURL.options);
  }
  // message is a request for the list of services
  else if (msgEvent.name === 'getServices')
  {
    msgEvent.target.page.dispatchMessage('setServices', LongURL.known_services);
  }
}

// validate whether or not the context menu item should be displayed
function validateContextMenu(event)
{
  if (event.userInfo === 'no')
  {
    event.target.disabled = true;
  }
}

// called when user selects our context menu item
function handleContextMenu(event) {
  if(event.command === 'expandurl')
  {
    safari.application.activeBrowserWindow.activeTab.page.dispatchMessage('expandurl', event.userInfo);
  }
}

// connect event listeners
safari.application.addEventListener('message', onRequest, false);
safari.application.addEventListener('validate', validateContextMenu, false);
safari.application.addEventListener('command', handleContextMenu, false);
safari.extension.settings.addEventListener('change', readSettings, false);

// initialize settings when Safari first loads
readSettings(null);

// get the list of services, we do this once when the extension loads (normally when Safari starts)
requestServices();

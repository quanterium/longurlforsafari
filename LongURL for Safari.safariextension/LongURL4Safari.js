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

// List of processed links for the current page
var waitingItems = {};

// local copies of options and known_services from global.html
var options = {};
var known_services = {};

var tooltip = 
{
  content: null, // tooltip div element
  create: function(tooltipWidth)
  {
    tooltip.content = document.createElement('div');
    tooltip.content.setAttribute('id', 'LongURL_tooltip');
    tooltip.content.style.position = 'absolute';
    tooltip.content.style.textAlign = 'left';
    tooltip.content.style.zIndex = '999';
    tooltip.content.style.wordWrap = 'break-word';
    tooltip.content.style.display = 'none';
    tooltip.content.style.opacity = '0.9';
    tooltip.content.style.backgroundColor = '#FFFF99';
    tooltip.content.style.width = tooltipWidth + 'px';
    tooltip.content.style.padding = '4px';
    tooltip.content.style['-webkit-border-radius'] = '15px';
    //document.body.insertBefore(tooltip.content, document.body.firstChild);
    document.body.appendChild(tooltip.content);
  },
  show: function(tinyurl)
  {
    var json = waitingItems[tinyurl].data;
    
    var temp = '<b>LongURL:</b> <a href="' + json['long-url'] + '" style="font-size:15px">' + json['long-url'] + '</a><br />';
    if(json['title'])
      temp += '<b>Title:</b> <span style="font-size:20px;color:#2200CC">'+json['title'] + '</span><br />';
    temp += '<br />';
    if(options.showShortUrl == 1)
      temp += '<b>ShortURL:</b> <span style="color:#008000">' + tinyurl + '</span><br />';
    if(json['meta-description'])
      temp += '<b>Description:</b> <span style="font-size:13px;color:#2200CC">'+json['meta-description'] + '</span><br />';
    if(json['all-redirects'] || json['content-type'] || json['rel-canonical'] || json['meta-keywords'])
      temp += '<br />';
    if(json['all-redirects'])
    {
      for(var m = 0; m < json['all-redirects'].length; m++)
      {
        temp += '<b>HTTP redirect:</b> <span style="color:#008000">' + json['all-redirects'][m] + '</span><br />';
      }
    }
    if(json['content-type'])
      temp += '<span style="font-size:9px;color:#2200CC"><b>Media type:</b> '+json['content-type'] + '</span><br />';
    if(json['rel-canonical'] || json['meta-keywords'])
      temp += '<br />';
    if(json['rel-canonical'])
      temp += '<b>Canonical URL:</b> '+json['rel-canonical'] + '<br />';
    if(json['meta-keywords'])
      temp +='<b>Keywords:</b> '+json['meta-keywords'] + '<br />';
    // Not shown : response-code (always 200 here)
    
    tooltip.content.innerHTML = temp; // Only one .innerHTML  = good perf.
    tooltip.content.style.display = 'block';
  },
  hide: function()
  {
    tooltip.content.style.display = 'none';
  }
}

function processBlacklistResult(data)
{
  if (data == 'allow')
  {
    // get the configuration options by sending a message to the global html page
    safari.self.tab.dispatchMessage('getOptions', null);
    console.log('[LongUrl] [Allow] Domain "' + document.domain + '" not found on blacklist');
  }
  else
  {
    // if not allowed, nothing else will happen
    console.log('[LongUrl] [Block] Domain "' + document.domain + '" matched blacklist with result: ' + data);
  }
}

function setOptions(data)
{
  options = data;
  // now we have the configuration options, get the list of services
  safari.self.tab.dispatchMessage('getServices', null);
}

function setServices(data)
{
  known_services = data;
  start();
}

function start()
{
  try
  {
    // Get data from global.html & process it
    var prepareRequest = function(a)
    {
      if(waitingItems[a.href]) // Is this url already there in the same page?
      {
        if(waitingItems[a.href].data == null) // Is this url currently processed?
        {
          var t = waitingItems[a.href].WItems;
          t[t.length] = a; // Add the link the the waitingItems list for future processing
        }
        else // Parse the link with the data previously stored
        {
          processHandler({'link': a.href, 'json':waitingItems[a.href].data});          
        }
        return; // don't even call background.html
      }
      
      // Add to the queue
      waitingItems[a.href] = {data: null, WItems: [a]};
      
      // Send a request to fetch data from the global html page.
      safari.self.tab.dispatchMessage('getLink', a.href);
    }
    
    //------------------------------
    
    // Will be called for every link in the page
    var checkLink = function(a)
    {
      if(a.getAttribute('checkLongURL'))
      {
        // Link already checked, stop here
        return;
      }
      else
      {
        // Preventing the link to be re-check
        a.setAttribute('checkLongURL', true);
        
        // What about cloned DOM nodes, doH!
        // If a copy of the a node is done before prepareRequest is executed, checkLongURL will prevent the copied item to be processed (when DOMNodeInserted will be fired).
      }
      
      // Get the link domain
      // Careful, maybe the link doesn't begin with 'http://' or 'www' or both...
      // This regex return false if the link is an anchor (href="#...") ; '#' won't match the pattern "[-\w]"
      // This regex return false if the link execute javascript (href="javascript:...") ; ':' won't match the pattern "[-\w]"
      // Nice js regex doc here : http://www.javascriptkit.com/jsref/regexp.shtml
      // Also useful : http://www.regextester.com/
      var regexResult = a.href.match(/^(?:https?:\/\/)?(?:www\.)?((?:[-\w]+\.)+[a-zA-Z]{2,})(\/.+)?/i);
      var domain = false;
      var params = false;
      if(regexResult)
      {
        // domain[0] == a.href ; We just want the domain ; obtained with domain[1] for that regex
        domain = regexResult[1];
        if(regexResult[2])
        {
          params = regexResult[2]; // There is some data (it's not simply the service url)
        }
      }
      
      // Only process links from a different domain and links corresponding to a kwon url shortener service
      if((domain !== document.location.host) && (typeof(known_services[domain]) !== 'undefined') && params)
      {
        var regex = new RegExp(known_services[domain]['regex'], 'i'); // Check link URL against domain regex
        if(!known_services[domain]['regex'] || a.href.match(regex))
        {
          prepareRequest(a);
        }
      }
    };
    
    //------------------------------
    
    // Listen for DOM modification (ajax request = potential shortened url)
    document.body.addEventListener('DOMNodeInserted', function(e)
    {
      // If the node as aldready been processed, do nothing :    
      if(e.target.id == 'LongURL_tooltip')
        return;
      
      var lookForA = function(n)
      {
        if(n.nodeName == 'A') // Found a link item (that you can click, not a simple url in the text)
        {
          checkLink(n);
        }
        for(var i = 0; i < n.childNodes.length; i++)
        {
          if(n.childNodes[i].nodeType == 1) // ELEMENT_NODE
          {
            lookForA(n.childNodes[i]);
          }
        }
      };
      lookForA(e.relatedNode); // Check children recursively, could slow down :-(
    }, false);
    
    //------------------------------
    
    if(options.showPopup)
    {
      // Create tooltip div (hidden)
      var tooltipWidth = 400;
      tooltip.create(tooltipWidth);
      
      // Give a name to the function for removeEventListener (see later)
      var ondocumentmovemouse = function(e)
      {
        var posx=0;var posy=0;
        var ev=(!e)?window.event:e;//Moz:IE
        if(ev.pageX){posx=ev.pageX;posy=ev.pageY}//Mozilla or compatible
        else if(ev.clientX){posx=ev.clientX;posy=ev.clientY}//IE or compatible
        else{return;}//old browsers
        
        if(tooltip.content)
        {
          tooltip.content.style.top = posy+20 + 'px';
          tooltip.content.style.left = posx-tooltipWidth/2 + 'px';
        }
      };
      
      // Set mousemove event for the tooltip
      document.body.addEventListener('mousemove', ondocumentmovemouse, false);
    }
    
    //------------------------------
    
    var links = document.evaluate('//a[@href]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); // XPath (faster)
    for(var i = 0; i < links.snapshotLength; i++)
    {
      checkLink(links.snapshotItem(i));
    }
  }
  catch(err)
  {
    console.log(options.logHeader + '[ERROR] ' + err);
  }
};


// this is the function that gets called when global html page sends us the
// result of a LongURL lookup
function processHandler(backResponse)
{
  var json = backResponse.json;
  var link = backResponse.link;
  
  // Utility function for mouseout listener
  var is_child_of = function(parent, child)
  {
    if(child != null)
    {      
      while(child.parentNode)
      {
        if((child = child.parentNode) == parent)
        {
          return true;
        }
      }
    }
    return false;
  }
  
  var parseLink = function(a)
  {
    if(typeof(a) != 'object') // asynchronous -> a could have been destroyed ; check if a is still here
    {
      throw('Current element is not and object');
    }
    
    // Copy the data, first 'if' may change the value ^^
    var tinyurl = a.href;
    
    if(options.replaceHref && json['long-url'])
    {
      // Whatever the content of the link is, we change the href attribute
      a.href = json['long-url'];
    }
    
    if(options.replaceVisibleHref > 0)
    {
      if(tinyurl == a.innerHTML || options.forceVisibleHref)
      {
        if(options.replaceVisibleHref == 1 && json['title'])
          a.innerHTML = json['title'];
        else if(json['long-url'])
          a.innerHTML = json['long-url'];
      }
    }
    
    if(options.showPopup)
    {
      a.addEventListener(
        'mouseover',
        function(e)
        {
          tooltip.show(tinyurl);
        },
        false
      );
      a.addEventListener(
        'mouseout',
        function(e)
        {
          // Mouseout is fired when moving to another element, even if the mouse stay inside the <a> :-(
          // We have to check if this event is really a mouseout for our <a> element            
          
          var current_mouse_target = null;
          if(e.toElement)
          {        
            current_mouse_target = e.toElement;
          }
          else if(e.relatedTarget)
          {        
            current_mouse_target = e.relatedTarget;
          }
          
          // Code inside this if is executed when leaving the link and it's children, for good
          if(a != current_mouse_target && !is_child_of(a, current_mouse_target))
          {
            tooltip.hide();
          }
        },
        false
      );
    }
  }
  
  //-------  
  //Syntax: waitingItems[a.href] = {data: null, WItems: []};
  
  try
  {
    waitingItems[link].data = json;
    
    // Loop trough each waiting items for this link
    for(var j = 0; j < waitingItems[link].WItems.length; j++)
    {
      // Process waiting item
      parseLink(waitingItems[link].WItems[j]);
      
      // Clear out
      waitingItems[link].WItems[j] = null;
      delete waitingItems[link].WItems[j];
    }
    
    // Final clear out from waiting list
    /* Still need data for tooltip
    waitingItems[link] = null;
    delete waitingItems[link];
    */
  }
  catch(err)
  {
    console.log(options.logHeader + '[ERROR] ' + err);
  }
}

// this handles messages from the global html page
function handleMessage(msgEvent)
{
  // LongURL lookup result
  if (msgEvent.name === 'lookupResult')
  {
    processHandler(msgEvent.message);
  }
  // blacklist check result
  else if (msgEvent.name === 'blacklistResult')
  {
    processBlacklistResult(msgEvent.message)
  }
  // configuration options being sent
  else if (msgEvent.name === 'setOptions')
  {
    setOptions(msgEvent.message);
  }
  else if (msgEvent.name === 'setServices')
  {
    setServices(msgEvent.message);
  }
}

if (window.top === window)
{
  // register the message handler
  safari.self.addEventListener('message', handleMessage, false);
  
  // find out if this domain is blocked by sending a message to the global html page
  safari.self.tab.dispatchMessage('checkBlacklist', window.top.document.domain);
}

// ]]>

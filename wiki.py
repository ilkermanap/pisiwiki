import os, sys, urllib2 as ur, urllib

#"https://web.archive.org/web/20120726004340/http://tr.pardus-wiki.org/Ana_Sayfa"

anasayfa = "https://web.archive.org/web/20130501202344/http://tr.pardus-wiki.org/Ana_Sayfa"
S = "https://web.archive.org"

DEBUG = 1

visitedLinks = ["deneme"]
visitedTitles = []

def writeFile(fname, output):
  listType = isinstance(output, list)
  strType = isinstance( output, str)
  fout = open("wiki/%s" % fname,"w")
  if strType == True:
    fout.write(output)
  if listType == True:
    for line in output:
      fout.write(line)
  fout.close()

def debug(paramName, val):
  if DEBUG == 1:
    print("DEBUG %s = %s" % (paramName, val))

def getUrl(url):
  url = url.replace("#038;","")
  url = url.replace("%26","&")
  url = url.replace("amp;","")
  
  debug("getUrl", url)
  try:
    return ur.urlopen(url).readlines()
  except:
    return None
    
def extractLink(line):
  title = ""
  tags = line.split('"')
  for tag in tags:
    if tag.find("tr.pardus-wiki.org") > -1:
      if tag.find("?") > -1:
        params = tag.split("?")[1].split("&")
        for param in params:
          if param.find("title") > -1:
            title = param.split("=")[1]
        return (tag, title)
      else:
        if tag.find("<a href") > -1:
          title = tag.split('"')[1].split("/")[-1]
        else:
          title = tag.split("/")[-1].split("#")[0]
        return (tag, title)
  return (None, None)
  
def getWikiText(s,t):
  if s.find(S) == -1:
    url = "%s%s" % (S, s)
    pageDate = s.split("/")[2]
  else:
    url = s
    pageDate = s.split("/")[5]

  fname =  "%s-%s" % (t,pageDate)
  fname = urllib.unquote(fname).decode('utf8')

  debug("getWikiText",url)
  page = getUrl(url)
  writeFile("%s.html" % fname, page)
  wiki = []
  found = False 
  for l in page:
    if found == True:
      wiki.append(l)
    if l.find("<textarea") > -1:
      debug("getWikiText", "%s  textarea BASLANGICI bulundu" % url)
      found = True
    if l.find("</textarea") > -1:
      debug("getWikiText", "%s  textarea BITISI bulundu" % url)

      found = False
      # url = urllib.unquote(url).decode('utf8')
      writeFile("%s.mediawiki" % fname, wiki)
      return 0
      
def links(content):
  t = []
  for l in content:
    if l.find('div id="p-personal"') > -1:
      return t

    if (l.find("Dosya:") == -1) and (l.find("a href") > -1) and (l.find("pardus-wiki.org") > -1):
      link = l.split('a href="')[1].split('"')[0]
      temp = "%s%s" % (S,link)
      if temp not in t:
        t.append(temp)
  return t

def getTextArea(link):
  s, t = extractLink(link)
  print t, visitedTitles
  if t not in visitedTitles:
    content = getUrl(link)
    for l in content:
      if l.find("action=edit") > -1:
        sourcePage, title = extractLink(l)
        if title not in visitedTitles:
          getWikiText(sourcePage, title)  
          visitedTitles.append(title)
          pageLinks = links(content)
          return pageLinks
      
#icerik = getUrl(anasayfa)
newLinks = getTextArea(anasayfa)
for link in newLinks:
  level2Links = getTextArea(link)
  try:
    for link2 in level2Links:
      print visitedTitles
      getTextArea(link2)
  except:
    continue
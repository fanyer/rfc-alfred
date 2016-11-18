#!/usr/bin/python
# coding=utf-8

import urllib2
import urllib
import json
import HTMLParser
import re
import alfred

################################################################################
def strip_html( html ):
    p = re.compile( r"<.*?>" )
    return p.sub( "", html )

def unescape_html( html ):
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape( html )

def parse_href( html ):
    link_begin = html.find( "<a href=\"http" )
    if link_begin == -1:
        return ""
    link_end = html.find( "\"" , link_begin+12 )
    if link_end == -1:
        return ""
    return html[link_begin+9:link_end]

################################################################################
def search_rfc( query ):
    result = []

    # params = { "q":query }
    # response = urllib2.urlopen( "https://m.zhihu.com/search?"+urllib.urlencode(params) ).read().split( "\n" )
    response = urllib2.urlopen( 'https://m.zhihu.com/search?q=%s' % query ).read()

    print(response)
    # response=response.decode('utf-8')
    title = ""
    link = ""
    answers = ""
    for line in response:
        # <a class="question_link" target="_blank" href="/question/{id}">{title}</a>
        # <a href="/question/{id}" class="answer zg-link-gray" target="_blank"><i></i>{answers}</a><a

        if "js-title-link" in line:
            title_begin = line.find( "\">" )
            title_end = line.rfind( "</a>" )
            if title_begin==-1 or title_end==-1:
                continue
            title = strip_html( line[title_begin+2:title_end] )

            if title!="" and link!="" and answers!="":
                result.append( alfred.Item( {"uid":alfred.uid(link), "arg":"http://www.zhihu.com/question/"+link},
                    unescape_html(unicode(title,"utf-8")), unicode(answers,"utf-8"), ("zhihu.png")) )

        else:
            continue



    return result



################################################################################
def main():
    ( param, query ) = alfred.args2()

    result = search_rfc( query )
    alfred.write( alfred.xml(result) )

if __name__ == "__main__":
    main()

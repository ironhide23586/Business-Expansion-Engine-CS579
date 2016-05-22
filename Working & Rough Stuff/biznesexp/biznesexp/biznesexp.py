import facebook

#token = 'CAACVpGIm9CMBAJg9ZCVXPC9ibXRryb0fg9eHN9eVS5HRQb5PqOTH8uGCsP0KWEQY6QDblR77TpbA8rBAouh3QZCwsaIKxerZAZC8EM0irsdPobRMtqaBPxuoMMAkDFhg90t2ZB6gjAJnaepCmYZAV5sSeFqPqKZCCR0yKD3DwOOohWODhBphgZAikin0Su9UZAhD7Qv4pSZBvUFVqbZASCZAOrT3'

#graph = facebook.GraphAPI(token)
#profile = graph.get_object("me")
#friends = graph.get_connections("me", "friends")

#friend_list = [friend['name'] for friend in friends['data']]

#print friend_list

import sys
import urllib2
import urllib
import json
import urlparse

def parse_str(str):
    nvps={};
    list = str.rsplit("&")
    for el in list:
        nvplist = el.rsplit("=")
        nvps[nvplist[0]]=nvplist[1]
    return nvps
 
def getAccessTokenDetails(app_id,app_secret,redirect_url,code):
 
    list ={}
    url =  "https://graph.facebook.com/oauth/access_token?client_id="+app_id+"&redirect_uri="+redirect_url+"&client_secret="+app_secret+"&code="+code;
    req = urllib2.Request(url)
    try: 
        response= urllib2.urlopen(req)
        str=response.read()
        #you can replace it with urlparse.parse_qs
        list = parse_str(str)
 
    except Exception, e:
        print e
    return list
 
def getUserDetails(access_token):
    list={}
    url = "https://graph.facebook.com/me?access_token="+access_token;
    req = urllib2.Request(url)
    try: 
        response= urllib2.urlopen(req)
        str=response.read()
        list = json.dumps(str)
    except Exception, e:
        print e
 
    return list
###########
 



APP_ID='164533253895203'
APP_SECRET='80d6caf901d8d923aef05de96158a232'
REDIRECT_URL='http://localhost:7724/biznesexp'

from bottle import Bottle, run, route, request
app = Bottle()

import webbrowser
webbrowser.open('https://www.facebook.com/dialog/oauth?client_id=164533253895203&scope=public_profile,email,user_friends&redirect_uri=http://localhost:7724/biznesexp')

CODE=''  ###HTTP GET Parameter received from Facebook 
details = None


@app.route('/biznesexp')

def my_listener():
    CODE = request.query.code
    details = getAccessTokenDetails(APP_ID,APP_SECRET,REDIRECT_URL,CODE)

    graph = facebook.GraphAPI(details['access_token'])
    profile = graph.get_object("me")
    friends = graph.get_connections("me", "friends")

    friend_list = [friend['name'] for friend in friends['data']]

    print friend_list

    #if not details["access_token"] is None:
    #    jsonText =getUserDetails(details["access_token"])
    #    #######Load it twice... Need to check
    #    jsonText =json.loads(jsonText)
    #    userInfo =json.loads(jsonText)
    #    #######Load it twice... Need to check
    #    print "Name: "+ userInfo['name']
    #    print "id: "+ userInfo['id']

    return 'Successfully logged in :D'
run(app, host="localhost", port=7724)
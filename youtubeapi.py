import requests
import youtube
import json
import re
import base64

apikey='AIzaSyB8MPxpE15KhpvUMo_SKSaljvw7H17Yvho'
def get_url_api(uid,part='',listing=False,token=''):
         if listing==False:
                  return 'https://www.googleapis.com/youtube/v3/videos?id='+uid+'&key='+apikey+'&part='+part
         else:
                  return 'https://www.googleapis.com/youtube/v3/playlistItems?playlistId='+uid+'&key='+apikey+'&part=id&maxResults=1&pageToken='+token


def get_video_info(url):
         uid = youtube.get_uid_from_url(url)
         if not uid:
                  return {}
         url_snippet = get_url_api(uid['uid'],part='snippet')
         
         resp = requests.get(url_snippet).text
         infos= json.loads(resp)
         url_duration = get_url_api(uid['uid'],part='contentDetails')
         duration_resp = requests.get(url_duration).text
         
         duration_info= json.loads(duration_resp)
         duration=duration_info['items'][0]['contentDetails']['duration']
         
         p = re.compile(r"(\d*)[HMS]")
         m = p.findall(duration)
         
         t=0
         for d in m:
                  t = t*60+int(d)
         duration= t
         
         ret = {}
         ret["url"]= url
         ret["uid"] = uid["uid"]
         ret["title"]=infos['items'][0]['snippet']['title']
         ret["description"] = infos['items'][0]['snippet']['description']
         ret["image_url"]=infos['items'][0]['snippet']['thumbnails']['high']['url']
         ret['duration'] = duration

         return ret

def get_video_infos_from_list(url):

         id_info= youtube.get_uid_from_url(url)
         if 'list' not in id_info:
                  return [get_video_info(url)]

         url_list=get_url_api(id_info['list'],listing=True)
         tokens=''
         while True:
                  url_list=get_url_api(id_info['list'],listing=True,token=tokens)
                  resp = requests.get(url_list).text
                  list_infos=json.loads(resp)

                  uid=str(base64.b64decode(list_infos['items'][0]['id']))
                  uid=list(map(str.strip,uid.split('.')))

                  url=youtube.get_url_with(uid[1].strip("'"))
                  

                  try:
                           yield get_video_info(url)
                  except Exception as e:
                           print('cannot get info from ' + url)
                           print(e)

                  if 'nextPageToken' in list_infos:
                           tokens=list_infos['nextPageToken']
                  else:
                           break



         
         
         



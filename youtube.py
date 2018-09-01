from urllib.parse import *
import requests
from pyquery import PyQuery as pq

def get_uid_from_url(url):
         ret= {}

         u = urlparse(url)
         if u.netloc == 'www.youtube.com':
                  qs = parse_qs(u.query)
                  if 'v' in qs:
                           ret['uid'] = qs['v'][0]
                  if 'list' in qs:
                           ret['list'] = qs['list'][0]
         elif u.netloc == 'youtu.be':
                  if u.path:
                           ret['uid'] = u.path[1:]

         return ret

def get_url_with(uid):
         return 'https://www.youtube.com/watch?v={}'.format(uid)

def get_video_info(url):

         uid = get_uid_from_url(url)

         if not uid:
                  return {}

         url = get_url_with(uid['uid'])

         resp = requests.get(url)
         h=pq(resp.text)
         w=resp.text
         with open("youtube.txt",'w',encoding="utf-8") as f:
                  f.write(w)
         n=h('meta[property="og:title"]')
         print(n)
         title = n and n[0].attrib['content'] or ''
         n=h('meta[property="og:description"]')
         content = n and n[0].attrib['content'] or ''
         n=h('meta[property="og:image"]')
         img_url = n and n[0].attrib['content'] or ''
         n=h('span.ytp-time-duration')
         duration = n and n[0].text or 0
         print(duration)
         if duration:
                  duration = list(map(str.strip,duration.split(':')))
                  t=0
                  for d in duration[:]:
                           t=t*60+int(d)
                  duration = t

         ret = {}
         ret["url"]= url
         ret["uid"] = uid["uid"]
         ret["title"]=title
         ret["description"] = content
         ret["image_url"]=img_url
         ret['duration'] = duration

         return ret

if __name__=='__main__':
         print(get_video_info('https://www.youtube.com/watch?v=mzJqxT1UGho'))

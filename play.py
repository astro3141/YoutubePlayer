from selenium import webdriver
import sys
import os.path
import time

curdir = os.path.join(os.path.dirname(__file__))
class MusicPlayer(object):

         def __init__(self):
                  self.driver = self._create_webdriver()

         def _create_webdriver(self):
                  if sys.platform == 'darwin':
                           driver = webdriver.Chrome(os.path.join(curdir,'webdriver','mac','chromedriver'))
                  elif sys.platform.startswith('linux'):
                           driver = webdriver.Chrome(os.path.join(curdir, 'webdriver','linux32','chromedrvier'))
                  elif sys.platform.startswith('win'):
                           driver = webdriver.Chrome(os.path.join(curdir,'webdriver','win','chromedriver.exe'))
                  else:
                           raise Exception('not support platform' + sys.platform)
                  return driver

         def play_url(self,url):
                  self.driver.get(url)
                  time.sleep(1)

         def _exec_js(self,js):
                  try:
                           ret = self.driver.execute_script(js)
                           return ret
                  except Exception as e:
                           if 'jQuery' in e.msg:
                                    self._injectJquery()
                                    return self._exec_js(js)
                           print(type(e))
                           print(e)

         def _injectJquery(self):
                  is_existed_Jquery = self._exec_js('return !!window.Jquery')
                  if not is_existed_Jquery:
                           #print('inject Jquery')
                           with open(os.path.join(curdir,'Jquery','Jquery-3.0.0.js')) as f:
                                    try:
                                              self._exec_js(f.read())
                                    except Exception as f:
                                                  prinf(f)
         def is_loaded(self):
                  ret = self._exec_js('''
                  return(funcion(){
                  try(
                           var v = jQuery(".video-stream.html5-main-video")[0];
                           return !!v;
                           }catch(e){
                           return false;
                           }
                  })();
                  ''')
                  print('is_loaded:',ret)
                  return ret

         def is_finished(self):
                  ret = self.exec_js('''
                  return(function(){
                  try{
                           var v = jQuery(".video-stream.html5-main-video")[0];
                           return v.duration > 0 && v.currentTime == v.duration;
                           }catch(e){
                           return true;
                           }
                  })();
                  ''')

                  return ret

         def skip_if_exists_ad(self):
                  try:
                           print('s')
                           ret=self._exec_js('jQuery(".adDisplay").hide()')
                           print(ret)
         
                           element=self.driver.find_element_by_css_selector(".videoAdUiPreSkipText.videoAdUiPreSkipTextForcedLineBreak")

                           while True:

                                    if '초 후 광고를' in element.text:
                                             print('s')
                                             time.sleep(5)
                                    else:
                                             element=self.driver.find_element_by_css_selector(".videoAdUiSkipButtonExperimentalText.videoAdUiFixedPaddingSkipButtonText")
                                             print('s')
                                             if ' 건너뛰기' in element.text:
                                                      element.click()
    
                  except Exception as e:
                           #pass
                           print(e)

         def play(self):
                  self._exec_js('jQuery(".video-stream.html5-main-video")[0].play()')

         def stop(self):
                  print(self._exec_js('return jQuery(".video-stream.html5-main-video")[0].pause();'))


         def is_unplable(self):
                  ret = self._exec_js('''
                  ret (function(){
                  try{
                  var v = jQuery("#unavailable-submessage").text().trim();
                  return v != '';
                  }catch(e){
                  return false;
                  }
                  })();
                  ''')

def play_starbuck_songs():
         """test music player,

         play starbuck songs to test musicplayer.
         """
         import time
         url = 'https://www.youtube.com/watch?v=mzJqxT1UGho&list=RDmzJqxT1UGho&start_radio=1'

         player = MusicPlayer()
         player.play_url(url)

         cur_url = None

         count = 0

         while True:
                  try:
                           if(count < 10):
                                    player.skip_if_exists_ad()
                                    url = player.current_url()
                                    if(cur_url != url):
                                             cur_url = url
                                    print(cur_url)

                           time.sleep(1)

                           if player.is_uplable():
                                    print('uplable')
                  except:
                           break

if __name__=='__main__':
         play_starbuck_songs()

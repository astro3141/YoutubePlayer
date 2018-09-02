import sqlite3
from datetime import datetime
from song import Song

DB_PATH = 'jukebox.db'



class Store(object):
         def __init__(self):
                  self.db = sqlite3.connect(DB_PATH,check_same_thread = False)
                  self._setup_db()

         def _setup_db(self):
                  self._setup_song_table()

         def _setup_song_table(self):
                  sql= '''\
create table if not exists SONGS(
                  id integer primary key autoincrement,
                  uid text unique,
                  title text,
                  artist text,
                  url  text,
                  img_url text,
                  played_count integer,
                  created_at datetime,
                  description text,
                  duration integer
);'''
 
                  cursor = self.db.cursor()
                  cursor.execute(sql)
                  cursor.close()
                  self.db.commit()

         def save(self,song):
                  cursor = self.db.cursor()
                  sql = '''\
insert into SONGS
                  (uid, title, artist, url, img_url, played_count, created_at, description,duration)
                  values(?,?,?,?,?,?,?,?,?)
'''

                  song.created_at = datetime.now()
                  data = (song.uid,song.title, song.artist, song.url, song.img_url,
                          song.played_count, song.created_at,song.description,
                          song.duration)

                  cursor.execute(sql,data)

                  cursor.close()
                  song.dbid = cursor.lastrowid
                  self.db.commit()

         def get_songs(self):
                  cursor = self.db.cursor()
                  sql = '''\
select id, uid, title, artist, url, img_url, played_count, created_at, description,
duration FROM SONGS
'''
                  cursor.execute(sql)
                  ret = []

                  while True:
                           data = cursor.fetchone()
                           if data:
                                    song = Song()

                                    song.dbid = data[0]
                                    song.uid = data[1]
                                    song.title = data[2]
                                    song.artist = data[3]
                                    song.url = data[4]
                                    song.img_url = data[5]
                                    song.played_count = data[6]
                                    song.created_at = data[7]
                                    song.description = data[8]
                                    song.duration = data[9]

                                    yield song

                           else:
                                    break
                  cursor.close()

         def update_or_new(self, song):
                  print(song)
                  if song.dbid:
                           print('update')
                           self.update(song)
                  else:
                           print('new')
                           self.save(song)

         def remove_all(self):
                  cursor = self.db.cursor()
                  sql = '''\
DELETE FROM SONGS;
'''
                  cursor.execute(sql)
                  cursor.close()
                  self.db.commit()

         def update(self, song):
                  cursor = self.db.cursor()
                  sql = '''\
update SONGS set uid=?, title=>, artist=?, url=?, img_url=?, played_count=?, description=?,
duration=? where id=?
'''
                  data = (song.uid, song.title, song.artist, song.url, song.img_url,
                          song.played_count, song.description, song.duration, song.dbid)

                  cursor.execute(sql,data)
                  cursor.close()
                  self.db.commit()

         def find_by_id(self, dbid):
                  cursor = self.db.cursor()
                  sql = '''\
select id, uid, title, artist, url, img_url, played_count, created_at, description, duration FROM SONGS where id=?
'''

                  cursor.execute(sql,(dbid, ))
                  data = cursor.fetchone()
                  if data:
                           song= Song()

                           song.dbid = data[0]
                           song.uid = data[1]
                           song.title = data[2]
                           song.artist = data[3]
                           song.url = data[4]
                           song.img_url = data[5]
                           song.played_count = data[6]
                           song.created_at = data[7]
                           song.description = data[8]
                           song.duration = data[9]

                  return song

         def find_by_uid(self, uid):
                  cursor = self.db.cursor()
                  sql = '''\
select id, uid, title, artist, url, img_url, played_count, created_at, description, duration FROM SONGS where uid=?
'''

                  cursor.execute(sql,(uid, ))
                  data = cursor.fetchone()
                  if data:
                           song= Song()

                           song.dbid = data[0]
                           song.uid = data[1]
                           song.title = data[2]
                           song.artist = data[3]
                           song.url = data[4]
                           song.img_url = data[5]
                           song.played_count = data[6]
                           song.created_at = data[7]
                           song.description = data[8]
                           song.duration = data[9]

                  return song

         def find_songs_by_title(self, title):
                  cursor = self.db.cursor()
                  sql = '''\
select id, uid, title, artist, url, img_url, played_count, created_at, description, duration FROM SONGS where title like ?
'''

                  cursor.execute(sql,(title, ))
                  ret = []
                  
                  for data in cursor.fetchmany(5):
                           if data:
                                    song= Song()

                                    song.dbid = data[0]
                                    song.uid = data[1]
                                    song.title = data[2]
                                    song.artist = data[3]
                                    song.url = data[4]
                                    song.img_url = data[5]
                                    song.played_count = data[6]
                                    song.created_at = data[7]
                                    song.description = data[8]
                                    song.duration = data[9]

                                    ret.append(song)

                  return ret


def test():
    from  song import Song
    print('i')
    store = Store()
    store.__init__()

    song = Song()
    song.title = "노래 제목"
    song.uid = 'uid01'
    song.url = "http://song_url"
    song.played_count = 1
    store.save(song)

    s = store.find_by_uid('uid01')
    print(s)

    for s in store.find_songs_by_title('%노래%'):
        print(s)

def test_get_songs():
    store = Store()
    for song in store.get_songs():
        print(song)
    

if __name__ == '__main__':
    test()
    test_get_songs()
                  

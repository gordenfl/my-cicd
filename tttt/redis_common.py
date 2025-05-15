# this file include all the function can write data and read data from Redis database
i# this file include all the function can write data and read data from Redis database
import time
import redis
from collections import defaultdict

# this is record for every user listen a music
# this record will composed with the data comes from music platform
class Record(object): 
    def __init__(self, user_id, song_id):
        self.user_id = user_id
        self.song_id = song_id
        self.timestamp = int(time.time())

    def set_song(self, song_id):
        self.song_id = song_id
    def set_user(self, user_id):
        self.user_id = user_id

    def get_time(self):
        return self.timestamp

# IMPORTANT!!!!
# Here we implement the write data and get data
class RedisMgr(object):
    def __init__(self, host="localhost", port=6379, db=1, count=10):
        self.host = host
        self.port = port
        self.db = db
        self.count = count
        self.delta = 60 # 60 seconds
        self.redis = redis.Redis(host='localhost', port=6379, db=1)

    # write data with the of user_id
    # the zadd means we want to add a new record of ZSet type, this type can easy to get the range of it's SCORE, that will give us a chance to get most recently song user listened.
    def write_data(self, record):
        key = f"user:{record.user_id}:songs"
        self.redis.zadd(key, {record.song_id:record.timestamp}) # here is the key point of the whole logic
        self.redis.expire(key, 60) #redis can set each value have an expire time, so we don't care about the data long time ago, it can let's system more lightly.

    
    def get_last_record(self, user_id):
        current_time = int(time.time())
        cutoff_time = current_time - self.delta # these two line just get the delta timestamp
        key = f"user:{user_id}:songs" #get the key
        songs = self.redis.zrangebyscore(cutoff_time, current_time)# IMPORTANT!!!, redis can using ZSet: Hash Table and Skip List
        #please remember the Skip List is high efficient data structure for search ordered data.

        #next is easy to understand, make a hash table, get how many count each song have been listened. sorted that and return the top 10 songs.
        song_count = defaultdict(int)
        for song in songs:
            song_count[song.decode('utf-8')] += 1
        
        sorted_songs = sorted(song_count.items(), key=lambda v:v[1], reverse=True)
        return sorted_songs[:self.count]
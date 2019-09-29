import argparse
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

import string
import redis
from flask import Flask, render_template, redirect
from flask import request
app = Flask(__name__)


class TinyURLRedis(object):
    def __init__(self, host='localhost', port=6379,password=''):
        try:
            pool = redis.ConnectionPool(host=host, port=port)
            self.r = redis.StrictRedis(connection_pool=pool)
        except Exception as e:
            print(e)

    def encode(self, longUrl, specify=None):
        def hash_units(dec, n=5):
            return abs(hash(dec)) % (10**n)
        if specify:
            suffix = specify
        else:
            suffix = str(hash_units(longUrl))
        if self.r.get(suffix) is None:
            self.r.set(suffix, longUrl)
        return suffix
    
    def decode(self, shortUrl):
        idx = shortUrl.split('/')[-1]
        if self.r.get(idx):
            return self.r.get(idx)
        else:
            return "Not exists such a url link"

class TinyURL(object):
    letters = string.ascii_letters + string.digits
    full_tiny = {}
    tiny_full = {}
    global_counter = 0
    
    def encode(self, longUrl):
        def decTo62(dec):
            result = ""
            while 1:
                result = self.letters[dec % 62] + result
                dec //= 62
                if not dec: break
            return result
        suffix  =decTo62(self.global_counter)
        if longUrl not in self.full_tiny:
            self.full_tiny[longUrl] = suffix
            self.tiny_full[suffix] = longUrl
            self.global_counter += 1
        else:
            suffix = self.full_tiny[longUrl]

        return suffix

    def decode(self, shortUrl):
        idx = shortUrl.split('/')[-1]
        if idx in self.tiny_full:
            return self.tiny_full[idx]
        else:
            return "Not exists such a url link"

parser = argparse.ArgumentParser()
parser.add_argument("--redis", default=True, action='store_true', help='using NoSQL-redis/hshTable for data saving.')
parser.add_argument("--ip", default='localhost', help='server ip.')
parser.add_argument("--port", default=5002, help='server port.')
args = parser.parse_args()
fun = TinyURLRedis() if args.redis else TinyURL()

@app.route('/shortURL', methods=['POST'])
def short_request():
    ServerPrefix = 'http://' + args.ip + ':' + str(args.port) + '/' 
    url = request.get_json()
    logging.info('ready for encoding ...')
    url_key = fun.encode(url)
    logging.info('after encoding:{}'.format(url_key))
    return  {'key': ServerPrefix + url_key}

@app.route('/<url_key>')
def redir(url_key):
    url = fun.decode(url_key)
    logging.info('after decoding:{}'.format(url))
    if url is None: return False
    return redirect(url)

@app.route('/specify/<specify_url>', methods=['POST'])
def specify(specify_url):
    ServerPrefix = 'http://' + args.ip + ':' + str(args.port) + '/' 
    url = request.get_json()
    logging.info('ready for encoding ...')
    url_key = fun.encode(url, specify_url)
    logging.info('after encoding:{}'.format(url_key))
    return  {'key': ServerPrefix + url_key}


@app.route('/')
def index():
    return render_template("index.html")

if __name__=='__main__':
    app.run(host=args.ip, port=args.port)
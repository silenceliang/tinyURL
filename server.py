import string
import redis
from flask import Flask, render_template, redirect
from flask import request
app = Flask(__name__)

class TinyURLRedis(object):
    def __init__(self, host='localhost', port=6379,password=''):
        self.letters = string.ascii_letters + string.digits
        try:
            self.r = redis.StrictRedis(host=host, port=port,password=password)
        except Exception as e:
            print(e)

    def encode(self, longUrl):
        def hash_units(dec, n=5):
            return abs(hash(dec)) % (10**n)
        ServerPrefix = "http://localhost:5002/"
        suffix = str(hash_units(longUrl))
        if self.r.get(suffix) is None:
            self.r.set(suffix, longUrl)

        return ServerPrefix + suffix
    
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
        ServerPrefix = "http://localhost:5002/"
        suffix  =decTo62(self.global_counter)
        if longUrl not in self.full_tiny:
            self.full_tiny[longUrl] = suffix
            self.tiny_full[suffix] = longUrl
            self.global_counter += 1
        else:
            suffix = self.full_tiny[longUrl]

        return ServerPrefix + suffix

    def decode(self, shortUrl):
        idx = shortUrl.split('/')[-1]
        if idx in self.tiny_full:
            return self.tiny_full[idx]
        else:
            return "Not exists such a url link"
''' Using hashTable (leetcode) '''
# fun = TinyURL()
''' Using Redis '''
fun = TinyURLRedis()

@app.route('/shortURL', methods=['POST'])
def short_request():
    url = request.get_json()
    print('ready for encoding ...')
    url_key = fun.encode(url)
    print('after encoding: ', url_key)
    return  {'key':url_key}

@app.route('/<url_key>')
def redir(url_key):
    url = fun.decode(url_key)
    print(url)
    if url is None: return False
    return redirect(url)

@app.route('/')
def index():
    return render_template("index.html")

if __name__=='__main__':
    app.run(host='localhost', port=5002)
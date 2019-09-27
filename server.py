import string
import redis
from flask import Flask, render_template, redirect
from flask import request
app = Flask(__name__)

class Redis(object):
    def __init__(self, host='localhost', port=6379,password=''):
        try:
            self.r = redis.StrictRedis(host=host, port=port,password=password)
        except Exception as e:
            print(e)
    
    def _put(self, key, value):
        return self.r.set(key,value)
    
    def _get(self, key):
        if self.r.get(key):
            return self.r.get(key)
        else:
            return "Not exist this URL !! "

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
        print(self.full_tiny)
        return "http://localhost:5002/" + suffix


    def decode(self, shortUrl):
        idx = shortUrl.split('/')[-1]
        if idx in self.tiny_full:
            return self.tiny_full[idx]
        else:
            return "Not exists such a url link"

fun = TinyURL()

@app.route('/shortURL', methods=['POST'])
def short_request():
    ServerPrefix = "http://localhost:" + str(5002) + "/"
    url = request.get_json()
    print('input url:', url)
    print('ready for encoding ...')
    url_key = fun.encode(url)
    print('after encoding: ', url_key)
    return  ServerPrefix + url_key

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
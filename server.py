import string
import redis
from flask import Flask, render_template, redirect
from flask import request
app = Flask(__name__)

class TinyURLRedis(object):
    def __init__(self, host='localhost', port=6379,password=''):
        self.letters = string.ascii_letters + string.digits
        self.global_counter = 0
        try:
            self.r = redis.StrictRedis(host=host, port=port,password=password)
        except Exception as e:
            print(e)

    def encode(self, longUrl):
        def decTo62(dec):
            result = ""
            while 1:
                result = self.letters[dec % 62] + result
                dec //= 62
                if not dec: break
            return result
        ServerPrefix = "http://localhost/"
        suffix = decTo62(self.global_counter)
        if self.r.get(suffix):
            self.r.set(suffix, longUrl)
            self.global_counter += 1
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

# fun = TinyURL()
fun = TinyURLRedis()

@app.route('/shortURL', methods=['POST'])
def short_request():
    url = request.get_json()
    print('input url:', url)
    print('ready for encoding ...')
    url = fun.encode(url)
    print('after encoding: ', url)
    return  url

@app.route('/specify/<url_key>')
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
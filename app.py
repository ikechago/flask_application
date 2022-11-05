# http://localhost:8000/

from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

# load html file.
with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()

routes = []

def route(path, method):
    routes.append((path, method))

route('/', 'index')
route('/index', 'index')
route('/next', 'next')

class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if(r[0] == _url.path):
                eval('self.' + r[1] + '()')
                break
        else:
            self.error()
        
    # index action
    def index(self):
        # レスポンスを送信して開始する
        self.send_response(200)
        # ヘッダー情報を完了する
        self.end_headers()
        html = index.format(
            title='Hello',
            message='ようこそ、HTTPServerの世界へ!'
        )
        self.wfile.write(html.encode('utf-8'))
        return
    
    def next(self):
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message='This is Next page.',
            data='{\n data:"this is data."\n}'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return



HTTPServer(('',8000), HelloServerHandler).serve_forever()
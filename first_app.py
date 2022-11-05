# p36

# http://localhost:8000/

# localhost:8000/next?id=123&pass=hoge&params=abs&params=xyz
# localhost:8000/index?id=123&pass=hoge&params=abs&params=xyz
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage

# load html file.
with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()


# ルーティング
routes = []

def route(path, method):
    routes.append((path, method))

route('/', 'index')
route('/index', 'index')
route('/next', 'next')
route('/xml', 'xml')


class HelloServerHandler(BaseHTTPRequestHandler):
    

    # ---------- GETメソッド ----------
    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if(r[0] == _url.path):
                eval('self.' + r[1] + '()')
                break
        else:
            self.error()
    
    

    # ---------- POSTメソッド ----------
    def do_POST(self):
        # FieldStorageインスタンスを用意する
        form = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})
        

        # 選択リスト
        if 'sel1' in form:
            items = str(form.getlist('sel1'))
        else:
            items = 'no-item'
        res = 'Select:' + str(items)


        # チェックボックス
        # if 'check1' in form:
        #     ck1 = True
        # else:
        #     ck1 = False
        # if 'check2' in form:
        #     ck2 = True
        # else:
        #     ck2 = False
        # res = 'Check1: ' + str(ck1) + ', Check2:' + str(ck2) 

        # ラジオボタン
        # if 'radio1' in form:
        #     r1 = form['radio1'].value
        # else:
        #     r1 = 'not selected'
        # res = 'Radio: ' + str(r1)

        
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message = res,
            data = form
        )
        self.wfile.write(html.encode('utf-8'))
        return



    # ---------- index action ----------
    def index(self):
        # レスポンスを送信して開始する
        self.send_response(200)
        # ヘッダー情報を完了する
        self.end_headers()

        html = index.format(
            title='Hello',
            message='Form送信'
        )
        self.wfile.write(html.encode('utf-8'))
        return
    


    # ----------next action----------
    def next(self):
        # _url = urlparse(self.path)
        # query = parse_qs(_url.query)
        # id = query['id'][0]
        # password = query['pass'][0]
        # msg = 'id=' + id + ', password=' + password
        self.send_response(200)
        self.end_headers()
        html = next.format(
            
            # message = msg,
            # data = query

            message = 'header data.',
            data = self.headers
        )
        self.wfile.write(html.encode('utf-8'))
        return



    # ----------error action----------
    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return



    # ----------xml action----------
    def xml(self):
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
        <data>
            <person>
                <name>Taro</name>
                <mail>taro@yamada</mail>
                <age>39</age>
            </person>
            <message>Hello Python!!</message>
        </data>'''
        self.send_response(200)
        # ヘッダー情報を送る
        # self.send_header('Content-Type','text/plain;charset=utf-8')
        self.send_header('Content-Type','application/xml;charset=utf-8')
        # ヘッダー終了
        self.end_headers()
        self.wfile.write(xml.encode('utf-8'))


HTTPServer(('',8000), HelloServerHandler).serve_forever()
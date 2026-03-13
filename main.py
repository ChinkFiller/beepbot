import webview
from api import WebApi
from flask import Flask, send_from_directory

server = Flask(
    __name__,
    static_folder='./webui',
    template_folder='./webui',
    static_url_path=""
)

# 首页
@server.route("/")
def index():
    return send_from_directory('./webui', 'index.html')

if __name__ == '__main__':
    window = webview.create_window(
        title='MIDI BOT',
        url=server,
        min_size=(1000,600),
        js_api=WebApi()
    )
    webview.start(debug=False)
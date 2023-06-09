from flask import Flask, request, abort, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageSendMessage
import qrcode
import uuid
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('settings.ini')
line_bot_api = LineBotApi(config['line']['access_token'])
handler = WebhookHandler(config['line']['secret'])
host = config['web']['host']


@app.route("/lineapi/qrgenerate/images/<filename>", methods=['GET'])
def return_qr_image(filename):
    return send_file(f'images/{filename}', mimetype='image/png')


@app.route("/lineapi/qrgenerate/", methods=['GET'])
def connection_test():
    return "qrgenerateサーバーは正常に作動しています。これはGETリクエストです。"


@app.route("/lineapi/qrgenerate/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    filename = f'img-{uuid.uuid4()}.png'
    qr = qrcode.make(event.message.text)
    qr.save(f'images/{filename}')
    img_url = f"https://{host}/images/{filename}"
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
    )


if __name__ == "__main__":
    app.run()

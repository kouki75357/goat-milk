from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 使用環境變數，避免硬編碼敏感資訊
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# Webhook 路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()
    if "羊奶" in user_message:
        reply_text = "您好！歡迎使用羊奶外送平台！請問您想要訂購羊奶還是查詢配送資訊？"
    elif "外送" in user_message:
        reply_text = "我們提供快速羊奶外送服務！請提供您的地址，我們會盡快安排配送。"
    elif "價格" in user_message:
        reply_text = "羊奶價格如下：\n- 500ml：$50\n- 1L：$90\n請問您要訂購哪一種？"
    elif "訂購" in user_message:
        reply_text = "請告訴我們您想要的羊奶數量和配送地址，我們會馬上為您處理！"
    else:
        reply_text = "您好！請問有什麼我可以幫您的？輸入「羊奶」或「外送」了解更多！"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Render 會提供 PORT 環境變數
    app.run(host='0.0.0.0', port=port)
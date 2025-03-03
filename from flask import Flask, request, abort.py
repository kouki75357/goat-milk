from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 填入你的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

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

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()  # 將訊息轉為小寫以便比對
    
    # 關鍵字回應邏輯
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

    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
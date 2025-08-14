from flask import Flask, request, abort
import requests, json

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='y+ZOY4eeH7rv8XXzByizvLDWpo389Qipebgx1cswl5C8qAguwDAJme6Xn+JXyExYeN4y4FaMqPNBJmLGW8Rl1vSNZmHKXgtCowL8uxkKVNYbHMRfi9rFxo/9a3d31Sf/pSbT4JKV/Ktmj/Key84r+gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7c15eb01c71b96f7ed03da87f2d25f0a')
llm_api_key = "sk-QR_3kckY-nDIjXnzZWtJNw"
modelname = "Google-Gemma-3-27B"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    response_from_llm = getllmresponse(event.message.text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response_from_llm)]
            )
        )

def getllmresponse(user_input, apikey=llm_api_key, modelname=modelname):
    url = "https://portal.genai.nchc.org.tw/api/v1/chat/completions"
    headers = {
        "x-api-key": f"{apikey}",  # 請填入你的 API 金鑰
        "Content-Type": "application/json"
    }
    data = {
        "model": f"{modelname}",
        "messages": [
            {
                "role": "user",
                "content": f"{user_input}"
            }
        ],
        "max_tokens": 10000,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content']
    else:
        result = f"Error: {response.status_code}. {response.text}"
    return result


if __name__ == "__main__":
    app.run()
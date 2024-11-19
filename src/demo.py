import os

import chainlit as cl
from dotenv import load_dotenv
from openai import OpenAI

# .envファイルのパス
dotenv_path = '/workspaces/rechatbot-demo/.env'
load_dotenv(dotenv_path)

# OpenAI APIキーを環境変数から取得
api_key = os.environ.get('OPENAI_API_KEY3')
if not api_key:
    raise ValueError("OpenAI API key not found. Make sure it is set in the .env file.")

# OpenAI APIキーを使用してクライアントを設定
client = OpenAI(api_key=api_key)
print(f"API Key: {api_key}")

@cl.on_chat_start
async def start():
    await cl.Message(content='こんにちは！どのようなお手伝いができますか？').send()

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
}

@cl.on_message
async def on_message(message: cl.Message):
    response = client.chat.completions.create(  # 修正ポイント
        model=settings["model"],
        messages=[{"role": "user", "content": message.content}],  # チャット形式でメッセージを指定
        max_tokens=150,
        temperature=settings["temperature"]
    )
    # messageはオブジェクトなので、.contentを使用
    content = response.choices[0].message.content
    if content is not None:
        await cl.Message(content=content.strip()).send()
    else:
        await cl.Message(content="申し訳ありませんが、返答が得られませんでした。").send()
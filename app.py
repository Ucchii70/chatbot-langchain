# 以下を「app.py」に書き込み
import streamlit as st
from langchain_openai import ChatOpenAI
# 人間がAIに送るメッセージとAIの初期設定のメッセージ
from langchain.schema import HumanMessage, SystemMessage
import os
import secret_keys  # 外部ファイルにAPI keyを保存(１つ下のコードに記載)

os.environ["OPENAI_API_KEY"] = st.secrets.OpenAIAPI.openai_api_key

chat = ChatOpenAI(model="gpt-3.5-turbo")

# streamlitのst.session_stateを使いメッセージのやりとりを保存, st.session_stateにmessageのキーがなければ下記スクリプトを実行
if "messages" not in st.session_state:
    st.session_state["messages"] = [
            SystemMessage(
                content="あなたは優秀なアシスタントAIです。"
                )
        ]

# LLMとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    # 人間がAIに送るメッセージ
    user_message = HumanMessage(
        content=st.session_state["user_input"]
    )

    messages.append(user_message)     # messagesにuser_messageを追加
    response = chat(messages)          # モデルに渡す
    messages.append(response)          # モデルから帰ってきたメッセージ(response)をmessagesに追加

    st.session_state["user_input"] = ""  # 入力欄を消去(普通に考えてlineとかと一緒。送信したら自分で入力した入力欄の文字を削除して初期状態にする)

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("From LangChain")

# ユーザーがテキスト入力フィールドに新しいメッセージを入力するたびに、そのメッセージがモデルに送信され、返答が取得されて画面に表示されるというフローが実現
user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 逆順でシステムメッセージ以外の直近のメッセージを上にしてループ
        speaker = "🙂" # ユーザーメッセージ
        if message.type == "ai": # メッセージタイプがaiであれば下記絵文字を表示
            speaker="🤖"

        st.write(speaker + ": " + message.content)

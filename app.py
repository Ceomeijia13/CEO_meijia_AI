import streamlit as st
import requests
import json

st.set_page_config(page_title="美甲AI聊天助手", page_icon="💬", layout="wide")
st.title("美甲店 AI 专属顾问 💬")

# 从保险箱里拿密钥
api_key = st.secrets["ZHIPU_API_KEY"]

# 1. 初始化“记忆盒子”（如果网页第一次打开，里面是空的，就给它塞一个默认提示）
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个专业的美甲店营销顾问，请用亲切、活泼的语气回答老板的问题。"}
    ]

# 2. 把之前的聊天记录全部显示在网页上（就像微信聊天界面）
for msg in st.session_state.messages:
    if msg["role"] != "system": # 系统的默认提示不显示给用户看
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 3. 在网页最下面生成一个聊天输入框
user_input = st.chat_input("请问老板，有什么我可以帮您的？")

# 4. 如果用户打字并回车了
if user_input:
    # 先把你（用户）的话显示在屏幕上
    with st.chat_message("user"):
        st.markdown(user_input)
    # 把你这句话存入记忆盒子
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 5. 呼叫 AI 大脑
    with st.chat_message("assistant"):
        with st.spinner("顾问思考中..."):
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            # 把整个记忆盒子（包括你刚说的话和之前的聊天记录）都发给AI
            data = {
                "model": "glm-4-flash",
                "messages": st.session_state.messages
            }
            payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
            response = requests.post(url, headers=headers, data=payload)
            result = response.json()

            # 6. 拿到回答，显示出来，并存进记忆盒子
            if 'choices' in result:
                ai_reply = result['choices'][0]['message']['content']
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                st.error(f"出错了：{result}")

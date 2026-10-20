import streamlit as st
st.set_page_config(page_title = "美甲AI营销",page_icon = "💅",layout = "wide")
import requests

# 设置网页标题
with st.sidebar:
    st.header("关于本工具")
    st.write("本工具由14岁CEO独立开发，专为美甲店老板打造。一键生成爆款文案，省下文案策划的钱。")
st.title("美甲店 AI 营销助手 💅")
st.write("欢迎老板！我是您的专属营销大师，输入款式，立刻为您生成爆款文案。")
#假如AI的回答存入了 answer 变量
if st.button("复制文案"):
    st.code(answer) #用代码框显示，右上角自带一个一键复制按钮

# 你的智谱 API Key
api_key = "f979c970ff634b218a3583c337f78b33.0v3v2N7cZDzqSFOW"

# 1. 网页上的下拉菜单（选择文案类型）
style_type = st.selectbox(
    "请选择你想生成的文案类型：",
    ("小红书种草文案", "朋友圈促销文案", "霸气开业宣传语")
)

# 2. 网页上的输入框（输入美甲款式）
user_input = st.text_input("请输入美甲款式（例如：法式、猫眼、碎钻）：")

# 3. 生成按钮
if st.button("一键生成文案 ✨"):
    if user_input == "":
        st.warning("神人，您还没输入款式呢！")
    else:
        with st.spinner("AI 正在疯狂码字中，请稍等..."):
            # 拼接给 AI 的指令
            prompt = f"你是一个顶尖的美甲店营销专家。请帮我为【{user_input}】款式写一段【{style_type}】。要求：语气吸引人，多用emoji，字数在150字左右。"
            
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "glm-4-flash",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
        
            #1.引入json库(如果最上面没写 import json，记得加上)
            import json
            #2.手动把字典中文不乱码的 JSON 字符串，并转成 utf-8 字节流
            payload = json.dumps(data,ensure_ascii = False). encode ('utf-8')
            #3.发送请求(注意把json=data，换成 data=payload)
            response = requests.post(url,headers = headers,data = payload)
            result = response.json()
            
            # 处理结果
            if 'choices' in result:
                st.success("文案生成完毕！直接复制带走：")
                # 用 st.markdown 显示，排版更好看
                st.markdown(result['choices'][0]['message']['content'])
            else:
                st.error(f"出错了：{result}")
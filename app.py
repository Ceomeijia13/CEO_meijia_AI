import streamlit as st
import requests
import json

# 1. 网页全局设置
st.set_page_config(page_title="美甲AI营销助手", page_icon="💅", layout="wide")

# 2. 侧边栏
with st.sidebar:
    st.header("👑 CEO 专属 AI 营销总监")
    st.write("本工具由13岁独立开发者打造。")
    st.write("专为美甲店老板一键生成小红书、朋友圈爆款文案，省下每月几千块的文案策划费。每天发3~5条朋友圈，吸引海量用户！")
    st.divider()
    st.caption("版本：v1.0 测试版")

# 3. 主体界面
st.title("美甲店 AI 营销助手 💅")
st.write("欢迎老板！我是您的专属营销大师。")

# 4. 创建标签页
tab1, tab2 = st.tabs(["🚀 小红书生成器", "📝 企业定制/联系老板 (开发中)"])

with tab1:
    # 5. 左右分栏：左边输入，右边输出
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("👈 输入需求")
        style_type = st.selectbox(
            "选择文案类型：",
            ("小红书种草文案","朋友圈促销文案", "霸气开业宣传语")
        )
        tone_type = st.selectbox(
        "选择文案语气：",("热情闺蜜风","高冷高级风","搞笑幽默风")
        )
        user_input = st.text_input("输入美甲款式（例如：法式、猫眼）：")
        #新加的：让老板自己填价格
    with st.expander("高级设置：添加促销价格(可选)"):
        original_price = st.text_input("原价（如：158）:",value="")
        promo_price = st.text_input("活动价（如：99）：",value="")
        generate_btn = st.button("一键生成文案 ✨", use_container_width=True)
        
    with col2:
        st.subheader("👉 AI 生成结果")
        if generate_btn and user_input:
            with st.spinner("AI 正在疯狂码字中..."):
                
                # 1. 商业防呆逻辑：判断用户到底有没有填价格
                if original_price and promo_price:
                    price_text = f"必须在文案中明确写出：原价 {original_price} 元，现在限时活动价只要 {promo_price} 元！"
                else:
                    price_text = "文案中不要提及任何具体价格，重点突出款式的美感和设计。"

                # 2. 把判断结果放进提示词里
                prompt = f"你是一个顶尖的美甲店营销专家。请帮我为【{user_input}】款式写一段【{style_type}】。要求：语气使用{tone_type}，多用emoji，字数在150字左右。{price_text}"
                
                # 3. 发送请求
                url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
                headers = {
                    "Authorization": f"Bearer {st.secrets['ZHIPU_API_KEY']}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "glm-4-flash",
                    "messages": [{"role": "user", "content": prompt}]
                }
                payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
                response = requests.post(url, headers=headers, data=payload)
                result = response.json()
                
                if 'choices' in result:
                    answer = result['choices'][0]['message']['content']
                    st.success("文案生成完毕！直接复制带走：")
                    st.code(answer,language="markdown")
                    st.snow()
                else:
                    st.error(f"出错了：{result}")
        elif generate_btn and not user_input:
            st.warning("老板，您还没输入款式呢！")
        else:
            st.info("请在左侧输入需求，点击生成。")

with tab2:
    st.write("企业定制目录，敬请期待！")

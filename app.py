import streamlit as st
import requests
import json

# ================= 1. 页面全局设置 =================
st.set_page_config(page_title="美甲AI营销助手", page_icon="💅", layout="wide")
# 初始化数据
if 'count' not in st.session_state:
    st.session_state.count = 0  # 今日生成篇数
if 'money' not in st.session_state:
    st.session_state.money = 0  # 累计省下的钱
# ================= 2. 侧边栏 =================
with st.sidebar:
    st.header("👑 CEO 专属 AI 营销总监")
    st.write("本工具由13岁独立开发者打造。")
    st.write("专为美甲店老板一键生成小红书、朋友圈爆款文案，省下每月几千块的文案策划费。")
    st.divider()
    st.caption("版本：v2.1 商业稳定版")

# ================= 3. 主体界面 =================
st.title("美甲店 AI 营销助手 💅")
# 顶部数据看板
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric(label="今日已生成文案", value=f"{st.session_state.count} 篇")
with col_m2:
    st.metric(label="累计为你省下文案费", value=f"¥ {st.session_state.money}")
st.write("欢迎老板！我是您的专属营销大师。")

# 创建标签页
tab1, tab2 = st.tabs(["🚀 小红书生成器", "📝 企业定制 (开发中)"])

with tab1:
    # 左右分栏
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("👈 输入需求")
        
        style_type = st.selectbox(
            "选择文案类型：",
            ("小红书种草文案", "朋友圈促销文案", "霸气开业宣传语")
        )
        
        tone_type = st.selectbox(
            "选择文案语气：",
            ("热情闺蜜风", "高冷高级风", "搞笑幽默风")
        )
        
        user_input = st.text_input("输入美甲款式（例如：法式、猫眼）：")
        
        # 折叠面板只装价格
        with st.expander("⚙️ 高级设置：添加促销价格（可选）"):
            original_price = st.text_input("原价（如：158）：")
            promo_price = st.text_input("活动价（如：99）：")
        
        # 按钮移出折叠框，直接放在最下面！
        generate_btn = st.button("一键生成文案 ✨", use_container_width=True)

    with col2:
        st.subheader("👉 AI 生成结果")
        
        if generate_btn:
            # ================= 商业防呆校验逻辑 =================
            if not user_input.strip():
                st.warning("老板，您还没输入美甲款式呢！")
                st.stop() # 停止往下执行
            
            # 检查价格是否合法
            price_text = "文案中不要提及任何具体价格，重点突出款式的美感和设计。"
            
            if original_price or promo_price:
                try:
                    op = float(original_price) if original_price else 0.0
                    pp = float(promo_price) if promo_price else 0.0
                    
                    if op < 0 or pp < 0:
                        st.error("老板，价格不能是负数哦！请重新输入。")
                        st.stop()
                    
                    # 如果活动价大于等于原价，给个提示，但不拦截
                    if op > 0 and pp > 0 and pp >= op:
                        st.warning("⚠️ 老板，您的活动价高于原价了哦！如果是反向整活营销，请忽略此提示。")
                        price_text = f"注意：这是一段反向营销/搞笑的整活文案。原价是 {op} 元，但活动价故意写成了 {pp} 元，请用极其夸张、幽默、反差的语气把这个离谱的价格写进去！"
                    elif op > 0 and pp > 0:
                        price_text = f"必须在文案中明确写出：原价 {op} 元，现在限时活动价只要 {pp} 元！"
                    elif op > 0:
                         price_text = f"必须在文案中明确写出：原价 {op} 元。"
                    elif pp > 0:
                         price_text = f"必须在文案中明确写出：现在限时活动价只要 {pp} 元！"
                         
                except ValueError:
                    st.error("老板，价格只能输入数字哦，请不要输入文字或符号！")
                    st.stop()
            # ====================================================

            # 正式调用
            with st.spinner("AI 正在疯狂码字中..."):
                # 增加对款式名称的长度限制，防止小作文（限制前20个字）
                safe_style = user_input[:20] 
                
                prompt = f"你是一个顶尖的美甲店营销专家。请帮我为【{safe_style}】款式写一段【{style_type}】。要求：语气使用【{tone_type}】，多用emoji，字数在150字左右。{price_text}"
                
                url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
                headers = {
                    # 警告：绝对不要在这里写明文密钥，必须用 st.secrets
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
                    
                    # ====== 新增的两行：一旦生成成功，数字自动增加 ======
                    st.session_state.count += 1
                    st.session_state.money += 50 # 假设每写一篇，帮老板省了50元外包费
                    # ==================================================
                    
                    st.success("文案生成完毕！直接复制带走：")
                    st.code(answer, language="markdown")
                    answer = result['choices'][0]['message']['content']
                    # 下雪特效
                    st.snow()
                else:
                    st.error(f"出错了，服务器返回：{result}")

with tab2:
    st.write("企业定制目录，敬请期待！")

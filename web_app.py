import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 介面設定
st.set_page_config(page_title="AI 英文單字助手", page_icon="📖")
st.title("📖 AI 英文影片單字助手")
st.caption("貼上字幕，點擊單字，AI 幫你做筆記！")

# API 設定
genai.configure(api_key="AIzaSyC83PWrwKxmVRN6cZjM3pptUYkKJkLP2Bo")

# 初始化 Session State (用來儲存選取的單字)
if 'words' not in st.session_state:
    st.session_state.words = []

# 左側邊欄：功能設定
with st.sidebar:
    st.header("設定")
    if st.button("清空選取單字"):
        st.session_state.words = []
        st.rerun()

# 主要介面
input_text = st.text_area("1. 請貼上 YouTube 字幕內容：", height=200)

# 模擬「點擊選詞」：在網頁版，手動輸入想學的詞最穩定
target_words = st.text_input("2. 想學的單字 (手動輸入或從下方挑選)：", value=", ".join(st.session_state.words))

if st.button("🚀 生成 AI 學習筆記", type="primary"):
    if not input_text:
        st.error("請先貼上字幕內容！")
    else:
        with st.spinner("AI 老師正在分析中..."):
            try:
                # 自動偵測模型
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                target_model = next((m for m in available_models if '1.5-flash' in m), available_models[0])
                model = genai.GenerativeModel(target_model)
                
                prompt = f"你是一位英文老師，請針對單字【{target_words if target_words else '由你挑選5個重點'}】結合以下內容製作筆記（單字、意思、原文、例句）：\n{input_text}"
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("📝 你的專屬筆記")
                st.markdown(response.text)
                
                # 提供下載按鈕
                st.download_button(
                    label="📥 下載筆記檔 (.txt)",
                    data=response.text,
                    file_name=f"English_Note_{datetime.now().strftime('%m%d')}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"發生錯誤: {e}")

st.info("💡 提示：在手機上打開網址，就能隨時練習喔！")
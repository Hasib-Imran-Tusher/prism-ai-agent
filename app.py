import streamlit as st
from google import genai
from google.genai import types
import base64
from datetime import datetime

# ============ পেজ কনফিগারেশন ============
st.set_page_config(
    page_title="Hasib Imran Tusher",
    page_icon="✨",
    layout="wide"
)

# ============ CSS ============
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a3e 0%, #2d1b5e 50%, #1e1e3f 100%);
    }
    html, body, [class*="css"], .stMarkdown, .stMarkdown p, 
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
    .stTextInput label, .stTextArea label, .stSelectbox label, 
    .stFileUploader label {
        color: #f8fafc !important;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 0.5rem 0;
        filter: drop-shadow(0 0 20px rgba(167, 139, 250, 0.5));
    }
    .subtitle {
        text-align: center;
        color: #e2e8f0 !important;
        font-size: 1.1rem;
    }
    .subtitle-tag {
        text-align: center;
        color: #a78bfa !important;
        font-size: 0.85rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #cbd5e1 !important;
        font-weight: 600;
        padding: 0 22px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #a78bfa) !important;
        color: #ffffff !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #a78bfa, #f472b6);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 700;
        width: 100%;
    }
    .stTextArea textarea, .stTextInput input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(167, 139, 250, 0.4) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 12px !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1633 0%, #0f0c29 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 16px;
        padding: 22px;
        margin: 12px 0;
    }
    .chat-user {
        background: linear-gradient(135deg, #6366f1, #a78bfa);
        color: #ffffff !important;
        padding: 14px 20px;
        border-radius: 18px 18px 4px 18px;
        margin: 10px 0 10px 20%;
    }
    .chat-ai {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(167, 139, 250, 0.3);
        color: #f8fafc !important;
        padding: 14px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 20% 10px 0;
    }
    .footer {
        text-align: center;
        color: #94a3b8 !important;
        padding: 20px 0;
        margin-top: 40px;
        border-top: 1px solid rgba(167, 139, 250, 0.15);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown('<h1 class="main-title">Hasib Imran Tusher</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Multimodal AI Agent — চিন্তা, দেখুন, বুঝুন</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-tag">✦ Powered by Gemini ✦</p>', unsafe_allow_html=True)

# ============ API Key সেটআপ ============
default_key = ""
try:
    default_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    default_key = ""

with st.sidebar:
    st.markdown("### ⚙️ সেটিংস")
    if default_key:
        api_key = default_key
        st.success("✅ API Key সংযুক্ত")
    else:
        api_key = st.text_input("🔑 Gemini API Key", type="password", value="")

    # দ্রুততম মডেল
    model_name = st.selectbox("🧠 মডেল", ["gemini-3.8-flash"])
    
    # ভাষা নির্বাচন
    language = st.selectbox("🌐 উত্তর ভাষা", ["Auto Detect", "বাংলা", "English"])
    
    st.divider()
    if st.button("🗑️ চ্যাট মুছুন"):
        st.session_state.chat_history = []
        st.rerun()
    if st.session_state.chat_history:
        chat_text = "\n\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])
        st.download_button("💾 চ্যাট সেভ", data=chat_text, file_name="chat.txt")
        st.caption(f"📊 {len(st.session_state.chat_history)} টি বার্তা")
    st.divider()
    st.caption("© ২০২৬ Hasib Imran Tusher")

if not api_key:
    st.markdown("""
    <div class="glass-card" style="text-align:center; margin-top:60px;">
        <h2 style="color:#a78bfa;">🔐 API Key দিন</h2>
        <p>বাম সাইডবারে আপনার Gemini API Key দিন।</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============ ফাস্ট ক্লায়েন্ট (Retry কমানো) ============
@st.cache_resource
def make_client(key):
    return genai.Client(
        api_key=key,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=2,
                initial_delay=0.5
            )
        )
    )

client = make_client(api_key)

# ============ ভাষার নির্দেশনা ============
def lang_instruction():
    if language == "বাংলা":
        return "সংক্ষেপে ও দ্রুত বাংলায় উত্তর দিন। "
    elif language == "English":
        return "Respond concisely in English. "
    return ""

# ============ ট্যাব ============
tab1, tab2, tab3 = st.tabs(["📝 টেক্সট চ্যাট", "🖼️ ছবি বিশ্লেষণ", "📄 PDF বিশ্লেষণ"])

# ---------- ট্যাব ১: চ্যাট (Streaming) ----------
with tab1:
    st.markdown("#### 💬 কথোপকথন")
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user"><strong>👤 আপনি</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai"><strong>🤖 AI</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

    prompt = st.chat_input("আপনার প্রশ্ন লিখুন...")
    
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="chat-user"><strong>👤 আপনি</strong><br>{prompt}</div>', unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            try:
                # Streaming এর মাধ্যমে দ্রুত রেসপন্স
                stream = client.models.generate_content_stream(
                    model=model_name,
                    contents=lang_instruction() + prompt
                )
                
                for chunk in stream:
                    if hasattr(chunk, 'text') and chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(f"**🤖 AI**\n\n{full_response}▌")
                
                placeholder.markdown(f"**🤖 AI**\n\n{full_response}")
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": full_response}
                )
            except Exception as e:
                err = f"❌ এরর: {str(e)[:200]}"
                placeholder.markdown(err)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": err}
                )
        
        st.rerun()

# ---------- ট্যাব ২: ছবি ----------
with tab2:
    st.markdown("#### 🖼️ ছবি বিশ্লেষণ")
    img_file = st.file_uploader("ছবি আপলোড করুন:", type=["jpg", "jpeg", "png", "webp"])
    img_prompt = st.text_input("প্রশ্ন:", value="এই ছবিতে কী আছে?")
    
    if img_file and st.button("🔍 বিশ্লেষণ", key="img_btn"):
        with st.spinner("বিশ্লেষণ করছি..."):
            try:
                img_b64 = base64.b64encode(img_file.read()).decode("utf-8")
                ext = img_file.name.split(".")[-1].lower()
                mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
                
                r = client.interactions.create(
                    model=model_name,
                    input=[
                        {"type": "text", "text": lang_instruction() + img_prompt},
                        {"type": "image", "data": img_b64, "mime_type": mime}
                    ]
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(img_file, use_container_width=True)
                with col2:
                    st.markdown(f'<div class="glass-card"><h4 style="color:#a78bfa;">🔍 বিশ্লেষণ</h4><p>{r.output_text}</p></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"এরর: {str(e)[:300]}")

# ---------- ট্যাব ৩: PDF ----------
with tab3:
    st.markdown("#### 📄 PDF বিশ্লেষণ")
    pdf_file = st.file_uploader("PDF আপলোড করুন:", type=["pdf"])
    pdf_prompt = st.text_input("প্রশ্ন:", value="এই PDF-এ কী আছে?")
    
    if pdf_file and st.button("📊 বিশ্লেষণ", key="pdf_btn"):
        with st.spinner("বিশ্লেষণ করছি..."):
            try:
                pdf_b64 = base64.b64encode(pdf_file.read()).decode("utf-8")
                
                r = client.interactions.create(
                    model=model_name,
                    input=[
                        {"type": "text", "text": lang_instruction() + pdf_prompt},
                        {"type": "document", "data": pdf_b64, "mime_type": "application/pdf"}
                    ]
                )
                st.markdown(f'<div class="glass-card"><h4 style="color:#a78bfa;">📊 বিশ্লেষণ</h4><p>{r.output_text}</p></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"এরর: {str(e)[:300]}")

st.markdown('<div class="footer">✨ Designed by <strong style="color:#a78bfa;">Hasib Imran Tusher</strong> — Powered by Gemini</div>', unsafe_allow_html=True)
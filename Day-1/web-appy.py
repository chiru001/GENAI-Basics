import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Boot
load_dotenv(override=True)
client = OpenAI()

st.set_page_config(
    page_title="Chat • Neat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Minimal, tight, readable styling
CSS = """
<style>
:root{
  --bg:#0d1224;        /* background */
  --panel:#121834;     /* panels/cards */
  --soft:#0f1630;      /* inputs */
  --border:#26335f;    /* borders */
  --text:#eef2ff;      /* main text */
  --muted:#a6b0d4;     /* muted text */
  --user:#1c3faa33;    /* user bubble */
  --assistant:#171f43; /* assistant bubble */
}
html, body, .stApp { background: var(--bg); color: var(--text); }
.main .block-container { max-width: 880px; padding-top: 12px; padding-bottom: 12px; }

.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.22);
}

/* Chat container: reduced height + tighter gaps */
# .chat-wrap{
#   background: var(--panel);
#   border: 0px solid var(--border);
#   border-radius: 12px;
#   padding: 6px 8px;
#   max-height: 55vh;
#   height: auto;            /* a bit shorter to remove extra white */
#   overflow-y: auto;
}
.chat { display:flex; gap:10px; align-items:flex-start; margin: 6px 0 10px; }

.avatar{
  flex:0 0 30px; height:30px; width:30px; border-radius:50%;
  display:grid; place-items:center; font-weight:700; color:#fff; font-size:0.8rem;
}
.user .avatar{ background: linear-gradient(135deg,#3b82f6,#06b6d4); }
.assistant .avatar{ background: linear-gradient(135deg,#8b5cf6,#ec4899); }

# .bubble{
#   background: var(--assistant);
#   border:1px solid var(--border);
#   border-radius:10px;
#   padding:8px 10px;        /* tighter padding */
#   line-height:1.45;        /* tighter line-height */
#   color: var(--text);
#   max-width: 100%;
#   word-wrap: break-word;
# }
.user .bubble{ background: var(--user); }

/* Clean markdown inside bubbles */
.bubble h1,.bubble h2,.bubble h3{ margin: 0.25rem 0; }
.bubble p{ margin: 0.2rem 0; }
.bubble ul, .bubble ol{ margin: 0.2rem 0 0.2rem 1.1rem; }
.bubble code{
  background:#0b132a; border:1px solid #2a3a6a; padding:1px 6px; border-radius:6px;
}
.bubble pre{
  background:#0b132a; border:1px solid #2a3a6a; padding:8px; border-radius:8px; overflow:auto; margin: 6px 0;
}

/* Input section compact + sticky */
.input-wrap{
  position: sticky; bottom: 0; z-index: 2;
  background: linear-gradient(180deg, rgba(13,18,36,0), var(--bg) 40%);
  padding-top: 6px;
}

/* Widgets: compact heights */
.stTextArea textarea{
  background: var(--soft) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  min-height: 80px !important;
}
.stButton>button{
  border-radius: 10px; border:1px solid var(--border);
  background: #1b254e; color: var(--text);
  height: 40px;
}
.stSelectbox > div > div{ color: var(--text); }
.small { color: var(--muted); font-size: 0.88rem; }
.hr { border: none; border-top: 1px solid var(--border); margin: 8px 0 10px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Utils
@st.cache_data(show_spinner=False)
def load_prompt():
    path = "./prompting/chain-of-thought.md"
    if not os.path.exists(path):
        return "You are a concise, helpful assistant."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def init_state():
    ss = st.session_state
    ss.setdefault("system_prompt", load_prompt())
    ss.setdefault("messages", [])
    ss.setdefault("model", "gpt-4.1")
    ss.setdefault("keep_history", True)
    ss.setdefault("max_pairs", 5)  # slightly less to keep responses snappy

def add(role, content):
    st.session_state.messages.append({"role": role, "content": content})

def build_window(latest_user=None):
    sys = {"role": "system", "content": st.session_state.system_prompt}
    if st.session_state.keep_history:
        k = st.session_state.max_pairs
        trimmed = st.session_state.messages[-(k*2):] if k > 0 else []
        out = [sys] + trimmed
        if latest_user:
            out.append({"role": "user", "content": latest_user})
        return out
    return [sys, {"role": "user", "content": latest_user or ""}]

def ask_openai(messages, model, temperature):
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=float(temperature),
        )
        return resp.choices[0].message.content, None
    except Exception as e:
        return None, str(e)

init_state()

# Sidebar (compact)
with st.sidebar:
    st.markdown("<div class='card'><b>Settings</b></div>", unsafe_allow_html=True)
    st.selectbox(
        "Model",
        ["gpt-4.1", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        index=0 if st.session_state.model not in ["gpt-4.1","gpt-4o","gpt-4o-mini","gpt-3.5-turbo"]
        else ["gpt-4.1","gpt-4o","gpt-4o-mini","gpt-3.5-turbo"].index(st.session_state.model),
        key="model",
    )
    st.toggle("Keep limited history", key="keep_history", value=st.session_state.keep_history)
    if st.session_state.keep_history:
        st.slider("Max pairs", 1, 10, st.session_state.max_pairs, 1, key="max_pairs")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    with st.expander("System prompt preview"):
        st.code(st.session_state.system_prompt[:6000], language="markdown")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Reload prompt"):
            st.session_state.system_prompt = load_prompt()
            st.success("Reloaded")
    with c2:
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.toast("Cleared")

# Header (tight)
st.markdown(
    "<div class='card' style='display:flex;justify-content:space-between;align-items:center;'>"
    "<div style='font-weight:800;font-size:1.15rem'>🧖‍♀️ Nani</div>"
    "<div class='small'>Fast, compact, readable</div>"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# Seed message
if not st.session_state.messages:
    add("assistant", "Hi! How can I help? 🙂")

# Chat area
st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    role, content = msg["role"], msg["content"]
    if role == "user":
        st.markdown(
            f"""
            <div class="chat user">
              <div class="avatar">U</div>
            #   <div class="bubble">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="chat assistant">
              <div class="avatar">AI</div>
              <div class="bubble">
            """,
            unsafe_allow_html=True,
        )
        # Let Streamlit render markdown cleanly
        st.markdown(content)
        st.markdown(
            """
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
st.markdown("</div>", unsafe_allow_html=True)

# Input (compact + sticky)
st.markdown("<div class='input-wrap'>", unsafe_allow_html=True)
with st.form("send", clear_on_submit=True):
    c1, c2 = st.columns([0.82, 0.18])
    with c1:
        user_text = st.text_area(
            "Message",
            height=90,
            placeholder="Type your message…",
            label_visibility="collapsed",
        )
    with c2:
        temp = st.slider("Temp", 0.0, 1.2, 0.7, 0.1, help="Higher = more creative")
        send = st.form_submit_button("Send ▶️", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Handle send
if send and user_text.strip():
    add("user", user_text.strip())
    msgs = build_window() if st.session_state.keep_history else build_window(user_text.strip())
    with st.spinner("Thinking…"):
        reply, err = ask_openai(msgs, st.session_state.model, temp)
    add("assistant", reply if (reply and not err) else f"Sorry, error: {err}")
    st.rerun()

# Footer (very small)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.markdown("<span class='small'>OPENAI_API_KEY from .env • Prompt: ./prompting/chain-of-thought.md</span>", unsafe_allow_html=True)

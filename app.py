import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# دیزاینی ڕووکار وەک ئەو وێنەیەی ناردووتە
st.set_page_config(page_title="Rabar AI | Gold Expert", page_icon="💰")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .chat-bubble { background-color: #1e2130; padding: 15px; border-radius: 15px; border: 1px solid #FFD700; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# وەرگرتنی داتا بەبێ API
@st.cache_data(ttl=300)
def get_gold_intel():
    symbols = {'Gold': 'GC=F', 'DXY': 'DX-Y.NYB', 'Oil': 'CL=F', 'BTC': 'BTC-USD'}
    data = {}
    for name, sym in symbols.items():
        data[name] = yf.Ticker(sym).history(period="2y", interval="1d")
    return data

def ai_predict(data_dict, days):
    df = data_dict['Gold'].copy()
    df['DXY'] = data_dict['DXY']['Close']
    df['Target'] = df['Close'].shift(-days)
    features = df[['Close', 'DXY']].dropna()
    target = df['Target'].loc[features.index].dropna()
    features = features.loc[target.index]
    model = RandomForestRegressor(n_estimators=50).fit(features, target)
    last_val = df[['Close', 'DXY']].iloc[-1].values.reshape(1, -1)
    return model.predict(last_val)[0]

# دەستپێکردنی بەرنامەکە
st.title("💰 Rabar AI - ڕاوێژکاری زێڕ")
st.write("---")

data = get_gold_intel()
current_p = data['Gold']['Close'].iloc[-1]

# لۆژیکی وەڵامدانەوە وەک چات
if "messages" not in st.session_state:
    st.session_state.messages = []

# وەڵامی سەرەتا
if not st.session_state.messages:
    welcome_msg = f"سڵاو، من Rabar AI م. نرخی ئێستای زێڕ ${current_p:.2f} دۆلارە. چۆن دەتوانم یارمەتیت بدەم لە پێشبینیکردن و شیکاری بازاڕ؟"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# شوێنی نووسینی پرسیار
if prompt := st.chat_input("لێرە پرسیار بکە (بۆ نموونە: پێشبینی هەفتەیەک)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # وەڵامی ژیری دەستکرد بەپێی پرسیارەکە
    with st.chat_message("assistant"):
        response = ""
        if "١٠ کاتژمێر" in prompt or "10" in prompt:
            res = ai_predict(data, 1)
            response = f"بەپێی شیکاری من، نرخی زێڕ بۆ ١٠ کاتژمێری داهاتوو نزیك دەبێتەوە لە ${res:.2f}."
        elif "٣ ڕۆژ" in prompt:
            res = ai_predict(data, 3)
            response = f"پێشبینی من بۆ ٣ ڕۆژی داهاتوو: ${res:.2f}. بازاڕ لەژێر کاریگەری پێوەری دۆلاردایە."
        elif "هەفتە" in prompt or "٧ ڕۆژ" in prompt:
            res = ai_predict(data, 7)
            response = f"ئامانجی هەفتانەی من بریتییە لە ${res:.2f}. ئاگاداری نرخی نەوت بە چونکە کاریگەری ڕاستەوخۆی هەیە."
        elif "مانگ" in prompt:
            res = ai_predict(data, 30)
            response = f"بۆ یەک مانگی داهاتوو، پێشبینی دەکەم نرخ بگاتە ${res:.2f}."
        else:
            response = "من لێرەم بۆ پێشبینیکردنی نرخی زێڕ. دەتوانیت بپرسیت دەربارەی (١٠ کاتژمێر، ٣ ڕۆژ، هەفتەیەک، یان مانگێک)."
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

# ڕێکخستنی شاشە
st.set_page_config(page_title="Rabar AI Mega Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0d12; color: #e0e0e0; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700; }
    </style>
    """, unsafe_allow_html=True)

ASSETS = {
    'زێڕ (XAU)': 'GC=F',
    'نەوت (Oil)': 'CL=F',
    'بیتکۆین (BTC)': 'BTC-USD',
    'ئیسریۆم (ETH)': 'ETH-USD',
    'سۆلانە (SOL)': 'SOL-USD'
}

@st.cache_data(ttl=300)
def fetch_mega_data():
    data_dict = {}
    for name, sym in ASSETS.items():
        ticker = yf.Ticker(sym)
        data_dict[name] = ticker.history(period="2y", interval="1d")
    data_dict['DXY'] = yf.Ticker('DX-Y.NYB').history(period="2y", interval="1d")
    return data_dict

def train_and_predict(asset_df, dxy_df, days):
    df = asset_df.copy()
    df['DXY'] = dxy_df['Close']
    df['Target'] = df['Close'].shift(-days)
    features = df[['Close', 'DXY']].dropna()
    target = df['Target'].loc[features.index].dropna()
    if len(features) < 10: return df['Close'].iloc[-1]
    features = features.loc[target.index]
    model = RandomForestRegressor(n_estimators=100, random_state=42).fit(features, target)
    last_val = df[['Close', 'DXY']].iloc[-1].values.reshape(1, -1)
    return model.predict(last_val)[0]

st.markdown("<h1 style='text-align: center; color: #FFD700;'>💎 Rabar AI Mega Professional</h1>", unsafe_allow_html=True)

try:
    all_intel = fetch_mega_data()
    dxy_data = all_intel['DXY']
    tabs = st.tabs(list(ASSETS.keys()))

    for i, asset_name in enumerate(ASSETS.keys()):
        with tabs[i]:
            df = all_intel[asset_name]
            curr_price = df['Close'].iloc[-1]
            p10h = train_and_predict(df, dxy_data, 1) * 0.9995
            p3d = train_and_predict(df, dxy_data, 3)
            p7d = train_and_predict(df, dxy_data, 7)
            p30d = train_and_predict(df, dxy_data, 30)
            p90d = train_and_predict(df, dxy_data, 90)

            c1, c2, c3, c4, c5 = st.columns(5)
            preds = [("١٠ کاتژمێر", p10h), ("٣ ڕۆژ", p3d), ("٧ ڕۆژ", p7d), ("١ مانگ", p30d), ("٣ مانگ", p90d)]
            for col, (lab, val) in zip([c1, c2, c3, c4, c5], preds):
                diff = val - curr_price
                col.metric(lab, f"${val:,.2f}", f"{diff:,.2f}")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index[-60:], y=df['Close'][-60:], name=asset_name, line=dict(color='#FFD700')))
            fig.update_layout(template="plotly_dark", height=350)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🤖Rabar ڕاوێژکاری ژیری دەستکرد")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "سڵاو چۆن یارمەتیت بدەم؟"}]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if prompt := st.chat_input("بپرسە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            res = "من لێرەم بۆ لێکدانەوەی بازاڕ. سەیری پێشبینییەکانی سەرەوە بکە بۆ هەر دراوێک."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

except Exception as e:
    st.error(f"هەڵەیەک ڕوویدا: {e}")

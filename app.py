import streamlit as st
import os, requests, openai

st.set_page_config(page_title="AI Trading Bot", layout="wide")
st.title("🚀 AI Trading Bot")

# Load API keys safely
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
alpha_key = st.secrets.get("ALPHAVANTAGE_KEY", "")

st.sidebar.header("Select Symbol & Actions")
symbol = st.sidebar.selectbox("Symbol", ["BTC/USDT", "ETH/USDT", "EUR/USD", "XAU/USD"])
if st.sidebar.button("🔄 Refresh"):
    st.experimental_rerun()

# Fetch live price
def get_price(sym):
    if sym.endswith("USDT"):
        resp = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym.replace('/','')}")
        return float(resp.json().get("price", 0))
    else:
        c1, c2 = sym.split("/")
        resp = requests.get(
            f"https://www.alphavantage.co/query",
            params={
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": c1,
                "to_currency": c2,
                "apikey": alpha_key
            }
        )
        return float(resp.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

price = get_price(symbol)
st.metric(f"{symbol} Price", f"{price:.5f}")

# GPT Insight
if st.button("Ask AI for Insight"):
    prompt = f"Analyze the market outlook for {symbol} at current price {price:.5f}"
    resp = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)
    st.markdown(f"**AI Insight:** {resp.choices[0].text.strip()}")

# Placeholder: Bitnode chart link
bitnode_url = f"https://bitnode.io/chart/{symbol.replace('/','-')}"
st.markdown(f"[📈 View {symbol} on Bitnode]({bitnode_url})")


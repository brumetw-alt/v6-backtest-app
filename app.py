import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 V6 回測系統（手機版）")

coins = st.multiselect(
    "選幣種",
    ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
    default=["BTCUSDT", "ETHUSDT"]
)

capital = st.number_input("資金", value=100)
leverage = st.slider("槓桿", 1, 200, 50)

def backtest(coin):
    np.random.seed(hash(coin) % 1000)
    returns = np.random.normal(0.002, 0.02, 200)

    equity = capital

    for r in returns:
        equity += equity * r * leverage

    roi = (equity - capital) / capital * 100
    return roi

if st.button("🚀 開始回測"):
    results = []

    for coin in coins:
        results.append({
            "coin": coin,
            "ROI": round(backtest(coin), 2)
        })

    df = pd.DataFrame(results)
    st.dataframe(df)
    st.bar_chart(df.set_index("coin"))

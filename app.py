import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 V6 回測系統（修正版）")

coins = st.multiselect(
    "選幣種",
    ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
    default=["BTCUSDT", "ETHUSDT"]
)

capital = st.number_input("資金", value=100)
leverage = st.slider("槓桿", 1, 50, 10)

def backtest(coin):

    np.random.seed(hash(coin) % 9999)

    returns = np.random.normal(0.001, 0.01, 200)

    balance = capital
    peak = capital
    trades = 0
    wins = 0

    equity_curve = []

    for r in returns:

        pnl = balance * r * leverage

        # 🛑 加入風控（關鍵）
        if pnl < -balance * 0.05:
            pnl = -balance * 0.05

        balance += pnl
        equity_curve.append(balance)

        peak = max(peak, balance)

        trades += 1
        if pnl > 0:
            wins += 1

        # ❗ 爆倉保護
        if balance <= capital * 0.2:
            break

    roi = (balance - capital) / capital * 100
    win_rate = wins / trades * 100
    drawdown = (peak - balance) / peak * 100

    return {
        "coin": coin,
        "ROI": round(roi, 2),
        "勝率": round(win_rate, 2),
        "回撤": round(drawdown, 2),
        "交易次數": trades,
        "最終資金": round(balance, 2)
    }

if st.button("🚀 開始回測"):

    results = []

    for coin in coins:
        results.append(backtest(coin))

    df = pd.DataFrame(results)

    st.subheader("📊 回測結果")
    st.dataframe(df)

    st.subheader("📈 ROI比較")
    st.bar_chart(df.set_index("coin")["ROI"])

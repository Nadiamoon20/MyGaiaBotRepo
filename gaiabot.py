# Title: GaiaAI Chatbot
# Created by: Moei
# Twitter: https://x.com/0xMoei

# The script will print the credit part and ask for the API key

import requests
import random
import time
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Configuration
BASE_URL = "https://traders.gaia.domains"  # ✅ Correct base URL
MODEL = "qwen2-0.5b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
    "How do institutional traders manage large positions without moving the market?",
    "What is the difference between liquidity takers and liquidity providers?",
    "How do interest rate differentials impact long-term currency trades?",
    "What are the key metrics to evaluate on-chain activity in crypto trading?",
    "How does order flow analysis improve trading precision?",
    "What is the concept of market microstructure?",
    "How do dark pools impact stock price discovery?",
    "What is a VWAP strategy and when is it effective?",
    "What is a TWAP strategy and how does it differ from VWAP?",
    "What are iceberg orders and how can they be detected?",
    "How do market makers hedge their exposure?",
    "What is gamma exposure and how does it impact market volatility?",
    "What is max pain theory in options trading?",
    "How does open interest affect futures and options markets?",
    "What is a volatility skew and what does it indicate?",
    "How is delta hedging used by professional traders?",
    "What is convexity in options pricing?",
    "What is a calendar spread and when is it used?",
    "How do synthetic positions work in options?",
    "How do quantitative traders use mean reversion strategies?",
    "What is statistical arbitrage and how does it function?",
    "How is cointegration used in pair trading strategies?",
    "What is a Z-score and how is it used in trading signals?",
    "How does machine learning apply to financial time series prediction?",
    "What are feature engineering techniques in algo trading?",
    "What is a walk-forward test in strategy validation?",
    "What is a Sharpe ratio vs. a Sortino ratio in performance measurement?",
    "How do traders deal with regime shifts in financial markets?",
    "What are structural breaks in time series analysis?",
    "What is the difference between drawdown and maximum drawdown?",
    "What is the Kelly Criterion and how can it optimize position sizing?",
    "What is expectancy in trading and how is it calculated?",
    "How do volatility clusters affect trade entries and exits?",
    "What is implied correlation and how is it used in multi-asset trading?",
    "What is fractal market theory and how does it differ from EMH?",
    "What is the Hurst exponent and how does it apply to trend analysis?",
    "How do volume profile and market profile differ?",
    "What is the concept of fair value in futures trading?",
    "What is delta-neutral trading and when is it used?",
    "What is vega in options trading and how is it hedged?",
    "What is theta decay and how can traders profit from it?",
    "How does backwardation and contango affect commodity trading?",
    "What are the major intermarket correlations used by traders?",
    "How do currency carry trades work and what are the risks?",
    "What is a funding rate in perpetual futures contracts?",
    "How does the basis relate to futures and spot prices?",
    "What is liquidity mining and how does it influence token prices?",
    "How do perpetual swaps differ from traditional futures?",
    "How is the efficiency of a trading system evaluated?",
    "What are the most common pitfalls in backtesting strategies?",
    "What are the statistical assumptions behind linear regression in trading?",
    "What are fat tails and why are they significant in trading models?",
    "How do black-box vs. gray-box models differ in algorithmic trading?",
    "What is the significance of kurtosis and skewness in return distributions?",
    "What is tail risk and how can it be managed?",
    "What is volatility targeting and how is it implemented?",
    "How do professional traders use implied volatility surfaces?",
    "What is the Greeks’ interplay in multi-leg options positions?",
    "How is sentiment data integrated into algorithmic models?",
    "What is a liquidity crisis and how can traders anticipate it?",
    "What is a risk parity strategy?",
    "How does portfolio rebalancing affect long-term performance?",
    "What are the implications of high-frequency trading (HFT) on retail markets?",
    "How do smart order routers function in modern trading systems?",
    "What are the common causes of slippage and how can it be reduced?",
    "How does trade latency impact execution quality?",
    "What is the impact of tick size on trading strategies?",
    "How are synthetic assets created on DeFi platforms?",
    "What is flash loan arbitrage in DeFi trading?",
    "What is sandwich attack in crypto trading?",
    "What are the mechanics of token burning and how does it affect price?",
    "How does dynamic pricing in AMMs (e.g., Uniswap) affect trade decisions?",
    "How is impermanent loss calculated in liquidity providing?",
    "What is rekt risk and how can it be mitigated in crypto leverage trading?",
    "How does a DAO’s treasury management impact token valuation?",
    "What is the role of social sentiment in meme coin trading?",
    "What is the impact of whale alerts on short-term crypto volatility?",
    "How can traders detect wash trading activity?",
    "What is the significance of GitHub activity in evaluating a crypto project?",
    "What is the difference between market beta and alpha?",
    "What is an overlay strategy in portfolio management?",
    "How is a Monte Carlo simulation used in trading systems?",
    "What are the advantages of ensemble models in trade signal generation?",
    "What are proprietary indicators and how are they developed?",
    "How does seasonality affect commodities and index trading?",
    "What is behavioral finance and how does it influence market anomalies?",
    "How does news sentiment scoring work in NLP-based trading systems?",
    "How are order book imbalance signals generated?",
    "What is the role of the Commitment of Traders (COT) report in futures trading?",
    "How do event-driven trading strategies operate?",
    "What is the significance of earnings surprise in equity trading?",
    "How does dividend yield impact stock price movement?",
    "What are the implications of quantitative tightening for traders?",
    "What is a convex strategy in portfolio construction?",
    "How does correlation breakdown impact hedge effectiveness?",
    "How do central clearing counterparties reduce systemic risk in derivatives markets?",
    "What is a fat-finger error and how do trading platforms prevent it?",
    "How do volatility-linked ETFs affect market dynamics?",
    "How can traders protect against currency exposure in global portfolios?",
    "What is ESG trading and how does it influence capital flow?",
    "What is the role of sentiment indexes like Fear & Greed in trade timing?",
    "What are the long-term effects of front-running on decentralized exchanges?"
]

def chat_with_ai(api_key: str, question: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": question}
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"Attempt {attempt+1} for question: {question[:50]}...")
            response = requests.post(
                f"{BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            logging.warning(f"API Error ({response.status_code}): {response.text}")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    raise Exception("Max retries exceeded")

def run_bot(api_key: str):
    while True:  # Outer loop to repeat the questions indefinitely
        random.shuffle(QUESTIONS)
        logging.info(f"Starting chatbot with {len(QUESTIONS)} questions in random order")

        for i, question in enumerate(QUESTIONS, 1):
            logging.info(f"\nProcessing question {i}/{len(QUESTIONS)}")
            logging.info(f"Question: {question}")

            start_time = time.time()
            try:
                response = chat_with_ai(api_key, question)
                elapsed = time.time() - start_time

                # Print the entire response
                print(f"Answer to '{question[:50]}...':\n{response}")

                logging.info(f"Received full response in {elapsed:.2f}s")
                logging.info(f"Response length: {len(response)} characters")

                time.sleep(QUESTION_DELAY)

            except Exception as e:
                logging.error(f"Failed to process question: {str(e)}")
                continue

def main():
    print("Title: GaiaAI Chatbot")
    print("Created by: Moei")
    print("Twitter: https://x.com/0xMoei")
    api_key = input("Enter your API key: ")
    run_bot(api_key)

if __name__ == "__main__":
    main()

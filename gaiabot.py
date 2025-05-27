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
BASE_URL = "https://traders.gaia.domains"
MODEL = "qwen2-0.5b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
    "What is trading, and how is it different from investing?",
    "What are the most common types of financial markets?",
    "What does risk management mean in trading?",
    "How does leverage impact a trade?",
    "What is a trading strategy, and why is it essential?",
    "What is a stop-loss order, and how does it work?",
    "What is take-profit in trading, and how is it used?",
    "How do traders use technical analysis?",
    "What are candlestick patterns and what do they indicate?",
    "What is fundamental analysis, and how does it apply to trading?",
    "What is a trading plan and why is it important?",
    "How can trading psychology affect decision-making?",
    "What is emotional trading and how can it be avoided?",
    "What is scalping in trading?",
    "What is day trading, and how does it differ from swing trading?",
    "What is swing trading, and when is it effective?",
    "What is position trading and who is it suitable for?",
    "How does market volatility impact trading?",
    "What are the key indicators used in technical analysis?",
    "What is volume in trading, and why does it matter?",
    "What is liquidity and how does it affect market behavior?",
    "How do support and resistance levels work?",
    "What is a trend line, and how is it drawn?",
    "What is a moving average, and how do traders use it?",
    "What is the RSI indicator, and what does it show?",
    "What is the MACD indicator used for?",
    "What is a trading signal?",
    "What is a breakout in trading?",
    "What is a false breakout and how can it be identified?",
    "What is a trading journal and how should it be maintained?",
    "What is backtesting and how can it improve a strategy?",
    "What are paper trading and demo accounts?",
    "What is margin trading, and what are its risks?",
    "What is short selling in trading?",
    "How do interest rates affect Forex trading?",
    "What is slippage in trading?",
    "What is a market order versus a limit order?",
    "What is an order book and how do traders use it?",
    "What is arbitrage in trading?",
    "What is high-frequency trading (HFT)?",
    "How do central bank decisions influence markets?",
    "What is a bull market and what characterizes it?",
    "What is a bear market and what are its signs?",
    "What are trading bots and how do they work?",
    "What is copy trading and how does it benefit beginners?",
    "What is the difference between spot and futures trading?",
    "What are derivatives in financial markets?",
    "What is hedging in trading?",
    "How do geopolitical events affect trading markets?",
    "How does economic news impact currency prices?",
    "What is a trading edge, and how can you develop one?",
    "What is diversification in trading portfolios?",
    "What are ETFs and how can they be traded?",
    "How do commodities like gold and oil react to inflation?",
    "What is a CFD (Contract for Difference)?",
    "What is a trading platform and how do you choose one?",
    "What is algorithmic trading?",
    "How do time frames affect trading decisions?",
    "What is a gap in the market and how is it traded?",
    "How is market sentiment analyzed?",
    "What is the importance of discipline in trading?",
    "What is a pump and dump scheme in crypto trading?",
    "How do tokenomics influence crypto asset valuation?",
    "What are ICOs and how do they relate to crypto trading?",
    "What is DeFi trading and how is it different from CeFi?",
    "What is impermanent loss in liquidity pools?",
    "What is staking and how is it different from trading?",
    "What are the biggest risks in crypto trading?",
    "What is trading volume and how is it measured?",
    "What are the differences between the NYSE and NASDAQ?",
    "How does after-hours trading work in the stock market?",
    "What are the risks of overtrading?",
    "What is FOMO in trading and how can it be avoided?",
    "How does correlation between assets affect portfolio management?",
    "What are synthetic assets in crypto?",
    "What is the VIX and what does it represent?",
    "What are flash crashes and what causes them?",
    "How does the halving event affect Bitcoin’s price?",
    "What is a rug pull in the crypto market?",
    "How do stablecoins influence trading behavior?",
    "What is the difference between hot wallets and cold wallets?",
    "What is front-running in trading?",
    "What is latency and how does it affect trade execution?",
    "What are futures contracts and how do they work?",
    "What is an options contract in trading?",
    "What are puts and calls in options trading?",
    "What is implied volatility in options trading?",
    "What is a trading pair in crypto exchanges?",
    "What is market capitalization and how is it used?",
    "What is a whale in crypto trading?",
    "How do you identify a good entry point in a trade?",
    "How do you know when to exit a trade?",
    "What is the Sharpe ratio in trading performance analysis?",
    "What is the difference between profit and ROI in trading?",
    "How can a trader build a diversified portfolio?",
    "What is the Pareto Principle in trading results?",
    "What is a black swan event in the markets?",
    "How important is news analysis for day traders?",
    "What are the best risk-to-reward ratios in trading?",
    "How can AI and machine learning be used in trading?",
    "How do market makers operate in different markets?",
    "What is a synthetic long or short position?",
    "How do interest rate swaps impact Forex markets?",
    "What is a trailing stop-loss and how is it used?",
    "How do you analyze candlestick wicks and bodies?",
    "What is the role of sentiment analysis in crypto trading?",
    "What is divergence in technical indicators and how is it interpreted?"
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

                # Ensure the script waits for the full response before proceeding
                time.sleep(QUESTION_DELAY)  # Wait before asking next question

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





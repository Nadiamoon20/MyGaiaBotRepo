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
BASE_URL = "https://internet.gaia.domains"
MODEL = "qwen2-0.5b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
    "What is an IP address, and how does it work?",
    "What is the difference between IPv4 and IPv6?",
    "How does a VPN protect your online privacy?",
    "What is DNS, and why is it important?",
    "How do cookies track user activity on websites?",
    "What is the difference between HTTP and HTTPS?",
    "What is cloud computing, and how does it work?",
    "How does data encryption protect information online?",
    "What is bandwidth, and why does it affect internet speed?",
    "How do search engines like Google rank websites?",
    "What is the role of a CDN (Content Delivery Network)?",
    "How does web hosting work?",
    "What are the main types of internet connections?",
    "How does a firewall enhance network security?",
    "What is a VPN?",
    "What is the function of a MAC address?",
    "What are the risks of using public Wi-Fi?",
    "What are the key differences between centralized and decentralized networks?",
    "What does ISP stand for?",
    "What does SSL stand for?",
    "What does TLS stand for?",
    "What does FTP stand for?",
    "What does API stand for?",
    "How do online ads use tracking pixels?",
    "What is web scraping, and is it legal?",
    "How do peer-to-peer (P2P) networks operate?",
    "How does a proxy server function?",
    "What is CSS, and how does it affect web design?",
    "What is IoT, and how does it connect devices?",
    "What is HTTP 404, and what does it indicate?"
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





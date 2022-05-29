import argparse
import requests
import time
import os, glob, random
from bs4 import BeautifulSoup
from icrawler.builtin import GoogleImageCrawler
from _thread import start_new_thread

from typing import (
    Optional
)
from telegram.utils import AsyncResult
from telegram.client import Telegram
from flask import Flask, request, jsonify

customCode = ""

class TelegramMyMod(Telegram):
          
    def _send_telegram_code(self, code: Optional[str] = None) -> AsyncResult:

        for x in range(10):        
            if customCode != "":
                code = customCode
                data = {'@type': 'checkAuthenticationCode', 'code': str(code)}
                return self._send_data(data, result_id='updateAuthorizationState')
            time.sleep(30)

        code = input("Enter code:")
        return self._send_data(data, result_id='updateAuthorizationState')
"""
Sends a message to a chat
Usage:
    python examples/send_message.py api_id api_hash phone chat_id text
"""

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/setCode/<code>', methods=['GET'])
def setCode(code):
    global customCode 
    customCode = code
    return "Code was set!"

@app.route('/control', methods=['POST'])
def control():
    content = request.json
    if content['mode'] == "on":
        start_new_thread(startQouter, ())

    return jsonify({"mode": content['mode']})

def startQouter():

    # parser = argparse.ArgumentParser()
    # parser.add_argument('api_id', help='API id')  # https://my.telegram.org/apps
    # parser.add_argument('api_hash', help='API hash')
    # parser.add_argument('phone', help='Phone')
    # parser.add_argument('chat_id', help='Chat id', type=int)
    # parser.add_argument('time_range', help='Duration in hours', type=int)
    args = {
        "api_id": "3740832",
        "api_hash": "9508678034db2a627c98773c1029bf2d",
        "phone": "+380955389871",
        "chat_id": "788665582",
        "time_range": 12 * 60 * 60
    }

    tg = TelegramMyMod(
        api_id=args["api_id"],
        api_hash=args["api_hash"],
        phone=args["phone"],
        database_encryption_key='changeme1234',
    )
    # you must call login method before others
    print("before login")
    res = tg.login()
    print(res)

    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    result = tg.get_chats()

    # `tdlib` is asynchronous, so `python-telegram` always returns you an `AsyncResult` object.
    # You can wait for a result with the blocking `wait` method.
    result.wait()

    if result.error:
        print(f'get chats error: {result.error_info}')
    else:
        print(f'chats: {result.update}')


    qouteURLs = ["https://citaty.info/movie/betmen-nachalo-batman-begins?page=1", "https://citaty.info/movie/betmen-nachalo-batman-begins", "https://citaty.info/movie/betmen-nachalo-batman-begins?page=2",
    "https://citaty.info/movie/temnyi-rycar-the-dark-knight", "https://citaty.info/movie/temnyi-rycar-the-dark-knight?page=1", "https://citaty.info/movie/temnyi-rycar-the-dark-knight?page=2", "https://citaty.info/movie/temnyi-rycar-the-dark-knight?page=3", 
    "https://citaty.info/movie/temnyi-rycar-vozrozhdenie-legendy-the-dark-knight-rises", "https://citaty.info/movie/temnyi-rycar-vozrozhdenie-legendy-the-dark-knight-rises?page=1", "https://citaty.info/movie/temnyi-rycar-vozrozhdenie-legendy-the-dark-knight-rises?page=2"]
    
    for URL in qouteURLs:
        parsedQoutes = []

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        qoute_blocks = soup.find("div", {"class":"view-content"}).find_all("div", {"class": "quotes-row"})

        # get qoutes 
        for qoute_block in qoute_blocks:
            qoute = qoute_block.find("p").text
            authorBlock = qoute_block.find("div", {"class": "field-type-taxonomy-term-reference"})
            author = authorBlock.find("div", {"class": "field-item"}).find("a").text if authorBlock != None else "" 
            parsedQoutes.append({
                "qoute": qoute + (("\n© " + author) if author != "" else ""),
                "author": author
            })
        
        # send qoutes depending on time
        for qouteObj in parsedQoutes:
            for x in range(1, 6):
                fileList = glob.glob("00000" + str(x) + ".*")
                if len(fileList) == 1:
                    os.remove(fileList[0])

            if qouteObj["author"] != "":
                google_Crawler = GoogleImageCrawler(storage = {'root_dir': './'})
                google_Crawler.crawl(keyword = qouteObj["author"] + " Нолан", max_num = 5)

                imgN = random.randint(1,5)
                if qouteObj["author"] == "Ра'с аль Гул":
                    imgN = 1
                elif qouteObj["author"] == "Люциус Фокс":
                    imgN = 1
                elif qouteObj["author"] == "Генри Дюкард (Henri Ducard)":
                    imgN = 4
                    

                imageFile = glob.glob("00000" + str(imgN) + ".*")[0]
                data = {
                        '@type': 'sendMessage',
                        'chat_id': args["chat_id"],
                        'input_message_content': {
                            '@type': 'inputMessagePhoto',
                            'photo': {
                                "@type": "inputFileLocal",
                                "path": imageFile
                            }
                        }
                    }
                r = tg._send_data(data)
                r.wait()
                time.sleep(3)

            result = tg.send_message(
                chat_id=args["chat_id"],
                text=qouteObj["qoute"]
            )
            result.wait()

            time.sleep(args["time_range"])
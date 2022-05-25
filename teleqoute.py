import argparse
import requests
import time
import os, glob, random
from bs4 import BeautifulSoup
from icrawler.builtin import GoogleImageCrawler

from telegram.client import Telegram

"""
Sends a message to a chat
Usage:
    python examples/send_message.py api_id api_hash phone chat_id text
"""


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('api_id', help='API id')  # https://my.telegram.org/apps
    parser.add_argument('api_hash', help='API hash')
    parser.add_argument('phone', help='Phone')
    parser.add_argument('chat_id', help='Chat id', type=int)
    parser.add_argument('time_range', help='Duration in hours', type=int)
    args = parser.parse_args()

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        database_encryption_key='changeme1234',
    )
    # you must call login method before others
    tg.login()

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


    qouteURLs = ["https://citaty.info/movie/betmen-nachalo-batman-begins?page=2", "https://citaty.info/movie/betmen-nachalo-batman-begins", "https://citaty.info/movie/betmen-nachalo-batman-begins?page=1",
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
            parsedQoutes.insert(0, {
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
                    imgN = 2
                elif qouteObj["author"] == "Люциус Фокс":
                    imgN = 1
                elif qouteObj["author"] == "Генри Дюкард (Henri Ducard)":
                    imgN = 4
                    

                imageFile = glob.glob("00000" + str(imgN) + ".*")[0]
                data = {
                        '@type': 'sendMessage',
                        'chat_id': args.chat_id,
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
                chat_id=args.chat_id,
                text=qouteObj["qoute"]
            )
            result.wait()

            time.sleep(args.time_range * 60 * 60)
import argparse
import requests
import time
from bs4 import BeautifulSoup


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
    parser.add_argument('text', help='Message text')
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

    # if result.error:
    #     print(f'get chats error: {result.error_info}')
    # else:
    #     print(f'chats: {result.update}')


    # URL = "https://citaty.info/movie/betmen-nachalo-batman-begins"
    # page = requests.get(URL)
    # soup = BeautifulSoup(page.content, "html.parser")
    # results = soup.find("div", {"class":"view-content"})
    # qoutes_elements = results.find_all("p")
    # for qoutes_element in qoutes_elements:
    #     print(qoutes_element.text + '\n')
        # result = tg.send_message(
        #     chat_id=args.chat_id,
        #     text=qoutes_element.text,
        # )
    # job_elements = results.find_all("div", class_="card-content")
    # for job_element in job_elements:
    #     title_element = job_element.find("h2", class_="title")
    #     company_element = job_element.find("h3", class_="company")
    #     location_element = job_element.find("p", class_="location")

    #     result = tg.send_message(
    #         chat_id=args.chat_id,
    #         text=title_element.text.strip(),
    #     )
    #     print(title_element.text.strip())
    #     print(company_element.text.strip())
    #     print(location_element.text.strip())
    #     print()
    
    # print(f'sc: {results.prettify()}')
    # result.wait()


    img_data = requests.get("https://itblog21.ru/wp-content/uploads/2020/02/jpg_jpeg01.jpg").content
    with open('test.jpg', 'wb') as handler:
         handler.write(img_data)

    data = {
            '@type': 'sendMessage',
            'chat_id': args.chat_id,
            'input_message_content': {
                '@type': 'inputMessagePhoto',
                'photo': {
                    "@type": "inputFileLocal",
                    "path":  "test.jpg"
                }
            }
        }
    r = tg._send_data(data)
    r.wait()

    
    result = tg.send_message(
        chat_id=args.chat_id,
        text="test2",
    )
    time.sleep(2.4)
    # if result.error:
    #     print(f'send message error: {result.error_info}')
    # else:
    #     print(f'message has been sent: {result.update}')
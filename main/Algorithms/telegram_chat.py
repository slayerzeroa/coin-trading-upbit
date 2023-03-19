import telegram
import asyncio
from reverse_timeseries_z_score import send

import sys, os
sys.path.append('../API')

from Get_Two_Close_Price import start

import time
import datetime
import schedule

def tel_go():
    upbit_path = "C:/Users/slaye/OneDrive/Desktop/upbit_environment/"
    env_list = ['TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID']

    for env in env_list:
        with open(upbit_path + f'{env}.txt') as keys:
            os.environ[env] = keys.read().strip()
    #telegram bot
    token = os.environ[env_list[0]]
    chat_id = os.environ[env_list[1]]

    start()
    message = send()

    async def main():
        bot = telegram.Bot(token=token)
        await bot.sendMessage(chat_id=chat_id, text=message)

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())


schedule.every(5).seconds.do(tel_go)
# schedule.every().day.at("09:00").do(tel_go)

while True:
    schedule.run_pending()
    time.sleep(1)
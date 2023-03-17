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
    #telegram bot
    token = '6221177240:AAEsdbSoiwoBgfyJEI5BYk9iMopfCeliFTk'
    chat_id = 6028514432

    start()
    message = send()

    async def main():
        bot = telegram.Bot(token=token)
        await bot.sendMessage(chat_id=chat_id, text=message)

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

schedule.every().day.at("9:00").do(tel_go)

while True:
    schedule.run_pending()
    time.sleep(1)
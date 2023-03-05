import telegram
import asyncio
#telegram bot


token = '6221177240:AAEsdbSoiwoBgfyJEI5BYk9iMopfCeliFTk'
chat_id = 6028514432


async def main():
    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chat_id, text="보낼 메세지")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
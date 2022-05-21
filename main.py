import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from menu import register_handlers_menu, set_commands
from quest import register_handlers_quest


async def main():
    bot = Bot(token="5343628425:AAGA9SgrATyJiqxHDDIUO4a3RDDiC8GCUiQ")
    dp = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_menu(dp)
    register_handlers_quest(dp)
    await set_commands(bot)
    await dp.skip_updates()
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())

import asyncio
import platform

import telegram_helper

if platform.system() == "Windows":
    # otherwise some "RuntimeError: Event loop is closed" occur
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

telegram_helper.run_bot()

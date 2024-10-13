"""
Module that containes main bot logic
"""


import logging
import os
import sys

from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import Update

from src.bot_functionality import echo, command_get_number


# Dotenv setup
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CREATOR_USER_ID = os.getenv('CREATOR_USER_ID')

# Logging setup
# It should save logs in stdout and in the file
logging.basicConfig(
    format='{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "msg": "%(message)s"}',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)
              , logging.FileHandler('bot.log')]
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main():
    """
    Main function in which the bot functionality is defined
    This simple bot just echos the user message
    """
    # Create the Application instance
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers which reacts on user input and uses functions from bot_functionality.py to process it
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Add handler for /get_number command
    application.add_handler(CommandHandler("get_number", command_get_number))

    # Saving information
    logger.info(f"Application handlers: {application.handlers}")

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info(f"Application polling: {application.run_polling(allowed_updates=Update.ALL_TYPES)}")

if __name__ == '__main__':
    main()

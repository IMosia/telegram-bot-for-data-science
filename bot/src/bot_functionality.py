"""
Module that contains functions which are responsible for bot functionality
"""

import os
import logging
import asyncpg
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn

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

# Dotenv setup
load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("DB_EXTERNAL_PORT")
DB_HOST = os.getenv("DB_HOST")
BACK_END_HOST = os.getenv('BACK_END_HOST')
BACK_END_PORT = int(os.getenv('BACK_END_PORT'))

############################################################################################################
# Supporting functionality
############################################################################################################

async def db_connect():
    """
    Function to connect to the database
    """
    try:
        connection = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
            port=DB_PORT,
            host=DB_HOST
        )
        logger.info("Connected to the database")
        return connection
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


async def call_back_end(request_type, request=None) -> dict:
    """
    Function to call the back-end service
    request - str or dict - request to the back-end service
    request_type - str - type of the request, can be:
        - "GET" - to get the data
        - "POST" - to send the data
        - "PUT" - to update the data
    """
    try:
        async with request_type(f"{BACK_END_HOST}:{BACK_END_PORT}/get_number") as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                logger.error(f"Error calling the back-end service: {response.status}")
                raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        logger.error(f"Error calling the back-end service: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


############################################################################################################
# Bot functionality
############################################################################################################

async def command_get_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Function to get a random number
    """
    try:
        data = await call_back_end("GET")
        await update.message.reply_text(f"Random number: {data['number']}")
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        await update.message.reply_text("Internal server error")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Echo the user message.
    """
    await update.message.reply_text(update.message.text)


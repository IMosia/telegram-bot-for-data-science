"""
Module for back-end logic
Working with FastAPI
"""

import logging
import sys
import random
import os
import dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn

# Logging setup
logging.basicConfig(
    format='{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "msg": "%(message)s"}',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('logs/back_end.log')]
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv.load_dotenv()
BACK_END_HOST = os.getenv('BACK_END_HOST')
BACK_END_PORT = int(os.getenv('BACK_END_PORT'))


async def process_request():
    """
    Module which handles the request
    It is a mock function that returns a random number
    If number % 3 == 0, it raises an exception
    """
    try:
        number = random.randint(0, 100)
        if number % 3 == 0:
            raise Exception("Number is divisible by 3")
        return number
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def create_app():
    """
    Function to create FastAPI application
    """
    app = FastAPI()

    @app.get("/get_number")
    async def get_number():
        """
        Function to get a random number
        """
        number = await process_request()
        return JSONResponse(content=jsonable_encoder({"number": number}))

    return app


if __name__ == '__main__':
    app = create_app()
    # Define host and port explicitly
    uvicorn.run(app, host=BACK_END_HOST, port=BACK_END_PORT)

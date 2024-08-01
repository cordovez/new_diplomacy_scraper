import beanie
import motor
import motor.motor_asyncio
from mongodb.models.models import (Country, Diplomat, Representation, MissionUnion,
                                   Embassy, Consulate)
from dotenv import load_dotenv
import os

load_dotenv()
"""Beanie uses a single model to create database models and give responses, so
models have to be imported into the client initialization.
    """
MONGO_URI = os.getenv("MONGO_URI")


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    await beanie.init_beanie(
        database=client["TEST"],
        document_models=[Country, Diplomat, Representation, MissionUnion, Embassy,
                         Consulate]
        )

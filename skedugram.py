import logging
import datetime
import dateparser
import re
import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

# Set up logging
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s)',
    level = logging.INFO
)
logger = logging.getLogger(__name__)
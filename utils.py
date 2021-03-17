import logging
import sys
from datetime import datetime

import praw


def initialize_logger_obj(logger_name):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def initialize_subreddit_obj(subreddit_name, praw_details):
    r = praw.Reddit(**praw_details._asdict())

    r.read_only = True
    return r.subreddit(subreddit_name)


def get_readable_datetime_from_timestamp(ts):
    return datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')

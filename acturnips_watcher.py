import os
from time import sleep

import telegram

import app_secrets
import utils
from objs import PrawDetails

SLEEP_TIME_IN_SECS = 10
SUBREDDIT_NAME = "acturnips"
TELEGRAM_CHANNEL = app_secrets.telegram_channel
FILE_NAME = os.path.basename(__file__).replace('.py', '')
MSG_DIVIDER = "~" * 25

bot = telegram.Bot(token=app_secrets.token)
logger = utils.initialize_logger_obj(FILE_NAME)
praw_details = PrawDetails(app_secrets.user_agent, app_secrets.client_id, app_secrets.client_secret)
subreddit = utils.initialize_subreddit_obj(subreddit_name=SUBREDDIT_NAME, praw_details=praw_details)


def get_latest_submission_id(subreddit_obj):
    latest_submission = list(subreddit_obj.new(limit=1))[0]
    logger.debug(f"First submission id is {latest_submission.id} | Title is {latest_submission.title}")
    return latest_submission.id


def prepare_msg_from_submission(submission):
    logger.info(f"\tSubmission title: {submission.title} | "
                f"Submitted time: {utils.get_readable_datetime_from_timestamp(submission.created_utc)}")
    return f"{submission.title}\n{submission.shortlink}\n{submission.selftext}\n{MSG_DIVIDER}\n"


if __name__ == '__main__':
    last_submission_id = get_latest_submission_id(subreddit)
    logger.debug(f"Sleep has been set to {SLEEP_TIME_IN_SECS} seconds")

    while True:
        submissions = list(subreddit.new(limit=5, params={'before': f"t3_{last_submission_id}"}))
        for s in submissions:
            bot.sendMessage(chat_id=TELEGRAM_CHANNEL, parse_mode=telegram.ParseMode.HTML,
                            text=prepare_msg_from_submission(s))

        if submissions:
            last_submission_id = submissions[0].id

        sleep(SLEEP_TIME_IN_SECS)

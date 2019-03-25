import logging
import sys
import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def get_user_name():
    return input('username: ')


def get_pwd():
    return input('password: ')


def view_bar(num, total):
    r = '\r%d/%d' % (num, total)
    sys.stdout.write(r)
    sys.stdout.flush()


def get_today():
    return datetime.datetime.utcnow()

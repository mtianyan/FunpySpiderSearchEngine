import pickle
import redis
import re
import hashlib

from config import REDIS_HOST, REDIS_PASSWORD


def get_md5(url):
    # str就是unicode了.Python3中的str对应2中的Unicode
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    # 从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def extract_num_include_dot(text):
    # 从包含,的字符串中提取出数字
    text_num = text.replace(',', '')
    try:
        nums = int(text_num)
    except:
        nums = -1
    return nums


def real_time_count(key, init):
    redis_cli = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD)
    if redis_cli.get(key):
        count = pickle.loads(redis_cli.get(key))
        count = count + 1
        count = pickle.dumps(count)
        redis_cli.set(key, count)
    else:
        count = pickle.dumps(init)
        redis_cli.set(key, count)

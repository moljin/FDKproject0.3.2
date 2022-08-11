import datetime
import os
from os.path import join, dirname

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_ROOT = os.path.join(BASE_DIR, 'templates')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

NOW = datetime.datetime.now()


dotenv_path = join(dirname(__file__), '.env')  # Path to .env file
load_dotenv(dotenv_path)


def read_secret(secret_name):
    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.rstrip().lstrip()
    file.close()
    return secret


class Config(object):
    DEBUG = False
    TESTING = False

    SESSION_COOKIE_NAME = 'FDK_project0.3'
    # TIMEZONE = datetime.datetime.now(timezone('Asia/Seoul'))
    TIMEZONE = 'Asia/Seoul'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465  # 587 : 이거는 장고
    MAIL_USERNAME = "khandure00@gmail.com"#"khandure05@gmail.com"
    MAIL_PASSWORD = "iccxyzmnkyfvszux"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    """
    MAIL_SERVER = "mw-002.cafe24.com"
    MAIL_PORT = 587
    MAIL_USERNAME = "rgmong@rgmong.kr"
    MAIL_PASSWORD = "ysh@981011"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
        """


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")  # 'thisissecretkey'
    SEND_FILE_MAX_AGE_DEFAULT = 1  # 개발환경에서 캐시 파일 1초마다 reload 할 수 있도록 한거다.
    TEMPLATES_AUTO_RELOAD = True  # DEBUG = True이면 자동으로 켜진다. 굳이 안써도 된다면서.....
    WTF_CSRF_ENABLED = True  # False로 하면 좋으나 체크하기위해 True

    MYSQL_ROOT_USER = 'root'
    MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD")# '981011'
    MYSQL_DATABASE = 'fdk_project0.3'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_ROOT_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8"


MYSQL_ROOT_PASSWORD = ''


class ProductionConfig(Config):
    # global MYSQL_ROOT_PASSWORD
    # try:
    #     if read_secret('SECRET_KEY'):
    #         SECRET_KEY = read_secret('SECRET_KEY')  # 'thisissecretkey'
    #     if read_secret('MYSQL_ROOT_PASSWORD'):
    #         MYSQL_ROOT_PASSWORD = read_secret('MYSQL_ROOT_PASSWORD')
    # except Exception as e:
    #     print(e)
    SECRET_KEY = 'thisissecretkey'

    MYSQL_ROOT_USER = 'root'
    MYSQL_ROOT_PASSWORD = 'moljin!981011'
    MYSQL_DATABASE = 'fdk_project0.3'
    MYSQL_HOST = '112.186.157.226'
    MYSQL_PORT = '56033'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_ROOT_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8"


class TestingConfig(Config):
    __test__ = False
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "sqlite_test.db")}'


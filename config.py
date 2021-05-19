import os


class Config(object):
    """
    Common configurations
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CSRF_ENABLED = True

    SESSION_COOKIE_SECURE = True

    SECRET_KEY = 'BC47E778683EA7B8DEAFF8C461BBEd'


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEVELOPMENT = True
    ENV = "development"
    SECRET_KEY = "secret_for_test_environment"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "9asdf8980as8df9809sf6a6ds4f3435fa64ˆGggd76HSD57hsˆSDnb"


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

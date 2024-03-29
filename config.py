import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    LOG_FILE  = "app.log"
    API_ACCESS_TOKEN = os.getenv('SECRET','Some_Predefined_Token')

    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://test:password@0.0.0.0:5432/cars_db"

    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://marco:foobarbaz@db:5432/testdb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'cars_db.db')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = False


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

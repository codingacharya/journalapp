import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cf7654709da7f63eb4c4e115bd217e9e4520d03ccbe16207ce8d3bf6e0e34965'

    # MySQL connection via XAMPP
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/journal_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

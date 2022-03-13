"""
Flask configuration
"""

SQLALCHEMY_DATABASE_URI = 'sqlite:///user_db.db'
SECRET_KEY = "rFsad!3dfs&df2$2###@@df"
# the below statement is added to suppress the deprecated warning
# issued by SQLAlchemy module
SQLALCHEMY_TRACK_MODIFICATIONS = False

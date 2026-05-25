
class Config:

    SQLALCHEMY_DATABASE_URI = \
    "mysql+pymysql://root:@localhost/travel_blog"
    # "mysql+pymysql://bloguser:StrongPass123@localhost/travel_blog"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
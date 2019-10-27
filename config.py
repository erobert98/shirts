import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SHOPIFY_SHARED_SECRET   = '438bc1a0829fc962c7879130694c785c'
    SHOPIFY_API_KEY         = '88a56f54b8b8afe3ed9159d650ab650c'
    SQLALCHEMY_DATABASE_URI = 'postgres://vghakumdtuyeaq:433dae02febdf40ff392094875fb70728f9ee9d5691c3668ab85b211cf1f1a01@ec2-174-129-18-42.compute-1.amazonaws.com:5432/d9dv2eptsnn6gm'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
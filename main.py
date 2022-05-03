from flask import Flask

from data import db_session
from api.main import api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(api)
    app.run()


if __name__ == '__main__':
    main()

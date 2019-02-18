from application import app
from database_manager import prepare_database


prepare_database()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

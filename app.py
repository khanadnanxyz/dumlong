import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def status():
    connection_info = False
    try:
        db.engine.connect()
        connection_info = True
    except BaseException as e:
        app.logger.info(e)
    finally:
        if connection_info:
            database = 'Connected'
        else:
            database = 'Please check database connection'
        data = {
            'status': 'OK',
            'database': database
        }
        return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

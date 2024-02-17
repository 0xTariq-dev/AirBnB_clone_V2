"""A simple Flask app with a single route."""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False, methods=['GET'])
def hello_hbnb():
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

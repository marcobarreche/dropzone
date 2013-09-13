from flask import Flask, render_template
import sys


app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def init():
    return render_template('uploader.html')


if __name__ == '__main__':
    ip, port = sys.argv[1].split(':')
    app.run(host=ip, port=int(port), debug=False)

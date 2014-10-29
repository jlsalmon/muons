from XRootD import client
from flask import Flask, render_template
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")

    with client.File() as f:
        f.open('root://localhost//tmp/event.txt')
        lines = f.readlines()



    templateData = {
        'title': 'HELLO!',
        'time': timeString,
        'lines': lines
    }

    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

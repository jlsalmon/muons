# from XRootD import client
from flask import Flask, render_template
from datetime import datetime
# import pygal
# from pygal.style import LightSolarizedStyle
# from detector import Event
import random

app = Flask(__name__)


@app.route("/")
def home():
    now = datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")

    # with client.File() as f:
    #     f.open('root://localhost//tmp/event.txt')
    #     events = list()
    #
    #     for line in f.readlines():
    #         event = Event()
    #         event.__dict__.update(json.loads(line))
    #         events.append(event)
    #
    # energies = list()
    # for event in events:
    #     energies.append(event.data[0] + random.random())
    #
    # bar_chart = pygal.Bar(style=LightSolarizedStyle)
    # bar_chart.add('Energies', energies)
    # chart = bar_chart.render(is_unicode=True)

    data = list()
    with open('test/test.txt', 'r') as f:

        bits = f.readline().split()
        previous = datetime.fromtimestamp(int(bits[0]) / 1e9)
        energy = ((int(bits[2]) + int(bits[4])) / 2) * 0.2
        data.append([0, energy])

        for line in f:
            bits = line.split()

            current = datetime.fromtimestamp(int(bits[0]) / 1e9)
            delta = current - previous
            delay = (delta.seconds * 1000.0) + (delta.microseconds / 1000.0)
            previous = current

            energy = ((int(bits[2]) + int(bits[4])) / 2) * 0.2
            data.append([delay, energy])

        # Make a copy and shuffle it
        data2 = data[:]
        random.shuffle(data2)

    templateData = {
        'title': 'Muon detector web interface',
        'time': timeString,
        # 'events': events,
        # 'chart': chart,
        'node_id': 10,
        'data': data,
        'data2': data2
    }

    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

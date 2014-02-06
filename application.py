from flask import Flask, render_template, request
from models import Spreadsheet
import re

app = Flask(__name__)


def validate(data):
    string_val = 0
    try:
        for i in data:
            i.strip()
            if i.startswith("'"):
                if not string_val:
                    string_val += 1
                else:
                    raise Exception('Unsupported operation for string type')
            elif i.startswith('='):
                eval(i.strip('='))
            elif i.startswith('-'):
                raise Exception('Unsupported value of the number')
            elif not re.match(r'^([0-9]+)([A-Z]+)$', i):
                raise Exception('Unsupported value')
    except Exception, e:
        return e
    return False


@app.route("/", methods=['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        data = Spreadsheet(request.values)


    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)

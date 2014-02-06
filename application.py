from flask import Flask, render_template, request, jsonify
from models import Spreadsheet
import re

app = Flask(__name__)


def validate(data):
    string_val = 0
    for i in range(len(data.data)):
        for j in range(len(data.data[i])):
            data.data[i][j].strip()
            if data.data[i][j]:
                if data.data[i][j].startswith("'"):
                    if not string_val:
                        string_val += 1
                    else:
                        data.result[i] = 'Unsupported operation for string type'
                elif data.data[i][j].startswith('='):
                    data.data[i][j] = eval(data.data[i][j].strip('='))
                elif not re.match(r'^([0-9]+)$', data.data[i][j]):
                    data.result[i] = 'Unsupported value of number'
    return data

def evaluate_data(data):
    for i in range(len(data.data)):
        if not data.result[i]:
            try:
                data.result[i] = eval(''.join(data.data[i]))
            except Exception, e:
                data.result[i] = unicode(e)
    return data.result


@app.route("/", methods=['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        data = Spreadsheet(request.values)
        if not data.unlinked:
            return jsonify(error = data.error)
        try:
            data = validate(data)
        except Exception, e:
            return jsonify(error = unicode(e))
        return jsonify(result = evaluate_data(data))
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)

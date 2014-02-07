from flask import Flask, render_template, request, jsonify
from models import Spreadsheet
import re, json

app = Flask(__name__)


def validate(data):
    for i in range(len(data.data)):
        string_val = 0
        for j in range(len(data.data[i])):
            if data.data[i][j]:
                if data.data[i][j].startswith("'"):
                    if not string_val:
                        string_val += 1
                        data.result[i] = data.data[i][j][1:]
                    else:
                        data.error[i] = 'Unsupported operation for string type'
                elif re.match(r'^=(\+|\-|\*|\/)$', data.data[i][j]):
                    data.data[i][j] = unicode(data.data[i][j][1:])
                elif re.match(r'^=([0-9]+)', data.data[i][j]):
                    try:
                        data.data[i][j] = unicode(eval(data.data[i][j][1:]))
                    except Exception:
                        data.error[i] = 'Unsupported expression'
                elif not re.match(r'[0-9]+', data.data[i][j]):
                    data.error[i] = 'Unsupported value of cell'
    return data


def evaluate_data(data):
    for i in range(len(data.data)):
        if i not in data.error.keys():
            try:
                eval_data = ''.join(data.data[i])
                if not eval_data.startswith("'"): data.result[i] = eval(eval_data) if eval_data else ''
            except Exception:
                data.result[i] = unicode('You have an error in the string. Please check it.')
        else:
            data.result[i] = data.error[i]
    return data.result


@app.route("/", methods=['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        data = Spreadsheet(request.values)
        if not data.unlinked:
            return jsonify(error = data.fata_error)
        try:
            data = validate(data)
        except Exception, e:
            return jsonify(error = unicode(e))
        return jsonify(result = evaluate_data(data))
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)

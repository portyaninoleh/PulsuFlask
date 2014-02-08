from flask import Flask, render_template, request, jsonify
from models import Spreadsheet
from main_types import StringType

app = Flask(__name__)

def evaluate_string(data_string):
    joined_string = u''.join([j.get_value for j in data_string])
    string_cells = [i for i in data_string if isinstance(i, StringType)]
    if not joined_string:
        return joined_string
    if [i for i in data_string if i.get_value.startswith('-')]:
        return 'Unsupported value of number'
    if string_cells:
        if len([i for i in data_string if i.get_value]) > 1:
            return 'Unsupported operation for string type'
        else:
            return string_cells[0].get_value
    else:
        return eval(joined_string)


@app.route("/", methods=['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        try:
            data = Spreadsheet(request.values)
        except RuntimeError:
            return jsonify(error = "You have linked cells to each other. Please refresh the table")
        # if isinstance(data, unicode):
        #     return jsonify(error = data)
        for i in range(len(data.data)):
            try:
                data.result[i] = evaluate_string(data.data[i])
            except Exception:
                data.result[i] = 'You have an error in your string'
        return jsonify(result = data.result)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)

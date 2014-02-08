import json, re
from main_types import factory


class Spreadsheet(object):

    def __init__(self, data):
        self.header = self.header_to_dict(json.loads(data['head']))
        self.data = self.convert_to_objects(json.loads(data['data']))
        self.result = dict()
        self.error = dict()

    def convert_to_objects(self, data):
        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = self.evaluate_cell(i, j, data)
        return data

    def header_to_dict(self, head):
        return {head[i]: i for i in range(len(head))}

    def evaluate_cell(self, row, col, data):
        col = self.header[col] if isinstance(col, unicode) else col
        pattern = re.compile('([0-9]+)([A-Z])+')
        result = data[row][col]
        if not isinstance(result, unicode):
            return result
        links = re.findall(pattern, result)
        if links:
            for pat in links:
                result_link = self.get_object(self.evaluate_cell(int(pat[0]) - 1, pat[1], data))
                result = result.replace(''.join(pat), result_link.get_value)
        return self.get_object(result)

    def get_object(self, val):
        if isinstance(val, unicode):
            if val.startswith("'"):
                return factory.get_type('string', val[1:])
            elif val.startswith('='):
                return factory.get_type('expression', val[1:])
            elif val is u'':
                return factory.get_type('empty_string')
            elif re.match(r'^[0-9]+$', val):
                return factory.get_type('int', val)
            else:
                return factory.get_type('expression', val)
        return val

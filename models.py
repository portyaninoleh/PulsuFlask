import json, re
from types import factory


class Spreadsheet(object):

    def __init__(self, data):
        self.data = json.loads(data['data'])
        self.header = self.header_to_dict(json.loads(data['head']))
        self.result = dict()
        self.error = dict()

    def header_to_dict(self, head):
        return {head[i]: i for i in range(len(head))}

    def evaluate_cell(self, row, col):
        col = self.header[col]
        result = self.data[row][col].strip("'")
        if re.match(r'^([0-9]+)([A-Z]+)$', result):
            result = self.evaluate_cell(int(re.split('([A-Z]+)$', self.data[row][col])[0]) - 1,
                                           re.split('^([0-9]+)', self.data[row][col])[-1])
        else:
            return result
        return result

    @property
    def unlinked(self):
        pattern = re.compile('([0-9]+)([A-Z])+')
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                links = re.findall(pattern, self.data[i][j])
                if links and not self.data[i][j].startswith("'"):
                    try:
                        for pat in links:
                            self.data[i][j] = self.data[i][j].replace(''.join(pat), self.evaluate_cell(int(pat[0]) - 1, pat[1]))
                    except RuntimeError:
                        self.fatal_error = u'You have linked cells to each other. Please correct your data'
                        return False
        return True


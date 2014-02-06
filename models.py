import json, re


class Spreadsheet(object):

    def __init__(self, data):
        self.data = json.loads(data['data'])
        self.header = self.headerToDict(json.loads(data['head']))
        self.result = list()

    def headerToDict(self, head):
        return {head[i]: i for i in range(len(head))}

    def evaluateCell(self, row, col):
        result = self.data[row][col]
        if re.match(r'^([0-9]+)([A-Z]+)$', self.data[row][col]):
            result = self.evaluateCell(self.header[re.split('^([A-Z]+)', self.data[row][col])[0]],
                                       self.header[re.split('^([0-9]+)', self.data[row][col])[0]])
        else:
            return result
        return result

    @property
    def unlinked(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                try:
                    self.data[i][j] = self.evaluateCell(i, j)
                except RuntimeError:
                    return 'You have linked cell to each other. Please correct this you data'

        return self.data


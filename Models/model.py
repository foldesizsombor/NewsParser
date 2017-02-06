class Model:
    _fields = {}
    _relatedTable = None

    def __init__(self, data=None):
        if self._relatedTable:
            self._populateFields()
            if data:
                self.setupWithDict(data)
        else:
            raise NotImplementedError("The child classes of the Model object should overwrite the _objectType field")

    def setupWithDict(self, data):
        for key in data.keys():
            if key in self._fields.keys():
                self._fields[key] = data[key]
            else:
                raise ValueError("The following field was not found in the object: " + str(key))

    def toDict(self):
        if self._fields:
            return self._fields
        else:
            return None

    def getField(self, field_name):
        return self._fields[field_name]

    def _populateFields(self):
        for row_name in self._relatedTable().getRowNames():
            self._fields[row_name] = None

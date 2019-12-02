class MongoObj(object):
    def __init__(self, field, value):
        self.value = value

        if isinstance(field, list):
            self.field = self.__getNestedFieldsStr(fields=[f.dbKey for f in field])
        else:
            self.field = field.dbKey

    def __getNestedFieldsStr(self, fields):
        return '.'.join(fields)


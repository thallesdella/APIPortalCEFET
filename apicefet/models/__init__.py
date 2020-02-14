import os
import json


class Model:
    def __init__(self, name):
        self.__create_db()
        self.__create_table(name)

    def dumps(self, data_id=None):
        table_data = self.__get_table_content()['data']
        if not data_id:
            return table_data

        position = 0
        for data in table_data:
            if data['id'] == data_id:
                return table_data[position]
            position += 1
        return []

    def loads(self, data):
        if not 'id' in data:
            return self.__add_data(data)
        return self.__update_data(data)

    def count(self):
        return len(self.__get_table_content()['data'])

    def __create_table(self, name):
        self.table = "{}/{}.json".format(self.db, name)

        if not os.path.exists(self.table):
            with open(self.table, 'w+') as table:
                table_content = json.dumps({'data': []}, indent=True)
                table.write(table_content)
        return

    def __create_db(self):
        self.db = "{}/../../db".format(os.getcwd())

        if not os.path.exists(self.db):
            os.makedirs('../../db')
        return

    def __get_table_content(self):
        with open(self.table, 'r') as table:
            table_content = json.load(table)
        return table_content

    def __add_data(self, data):
        data_id = 1
        data.update({'id': data_id})

        table_content = self.__get_table_content()
        if not table_content['data']:
            table_content['data'] = [[*data]]
        else:
            table_content['data'] = [*table_content['data'], [*data]]

        with open(self.table, 'w') as table:
            db_data = json.dumps(table_content, indent=True)
            table.write(db_data)
        return data_id

    def __update_data(self, data):
        pass

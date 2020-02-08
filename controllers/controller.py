from flask import Blueprint


class Controller:

    def __init__(self, name, import_name):
        bp = Blueprint(name, import_name)

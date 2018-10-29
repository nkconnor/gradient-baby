import hug
import os
from jinja2 import Template

class View:
    @staticmethod
    def render(name, **kwargs):
        with open("./templates/"+name+".html") as fh:
            template = Template(fh.read())

        return template.render(kwargs)

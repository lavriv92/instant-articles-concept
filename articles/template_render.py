import os.path
import logging
import tornado.template


class TemplateRenderer(object):

    def __init__(self, path):
        self.path = path

    async def _get_template(self, name):
        file_path = os.path.join(self.path, name)
        with open(file_path) as f:
            return f.read()

    async def __call__(self, template_name, **data):
        template_string = await self._get_template(template_name)
        return tornado.template.Template(template_string).generate(**data)

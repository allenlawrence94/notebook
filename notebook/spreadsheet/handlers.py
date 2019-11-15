from ..base.handlers import path_regex, IPythonHandler
from tornado import web
from notebook.utils import maybe_future
import json


class SpreadsheetHandler(IPythonHandler):

    @web.authenticated
    def get(self, path):
        # /files/ requests must originate from the same site
        self.check_xsrf_cookie()
        cm = self.contents_manager

        if cm.is_hidden(path) and not cm.allow_hidden:
            self.log.info("Refusing to serve hidden file, via 404 Error")
            raise web.HTTPError(404)

        path = path.strip('/')
        if '/' in path:
            _, name = path.rsplit('/', 1)
        else:
            name = path

        model = yield maybe_future(cm.get(path, type='file', content=True))

        if self.get_argument("download", False):
            self.set_attachment_header(name)

        self.set_header('Content-Type', 'application/json')

        self.write(
            self.render_template(
                'spreadsheet.html',
                spreadsheet_data=json.dumps(model['content'])
                # notebook_name=name,
                # kill_kernel=False,
                # mathjax_url=self.mathjax_url,
                # mathjax_config=self.mathjax_config,
                # get_frontend_exporters=get_frontend_exporters
            )
        )


default_handlers = [
    (r"/spreadsheets%s" % path_regex, SpreadsheetHandler),
]

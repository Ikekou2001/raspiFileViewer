class ObjDict(dict):
  def __call__(self, __obj):
    self[__obj.__name__] = __obj
obj = ObjDict()

import builtins
import io

from .db import *

obj(builtins)

from pathlib import Path
import flask

STATIC_FOLDER = Path("resource")
FILEROOT = STATIC_FOLDER / "file"
app = flask.Flask(__name__,
                  static_folder=STATIC_FOLDER)

database = DB(app.static_folder)

@app.route("/")
def index():
  return flask.redirect("/l")

@app.route("/l/")
@app.route("/l/<title>")
def l_title(title: str | None = None):
  strio = io.StringIO()
  strio.writelines(
    line for line in io.StringIO(
      flask.render_template(
        "list.jinja2", **obj,
        list = database.list(title)
      )
    ) if not line.isspace()
  )
  return strio.getvalue()

@app.route("/v/<title>")
@app.route("/v/<title>/<int:vol>")
def v(title: str, vol: int = 1):
  view = database.view(title, vol)
  strio = io.StringIO()
  strio.writelines(
    line for line in io.StringIO(
      flask.render_template(
        "view.jinja2",
        **obj,
        view = view
      )
    ) if not line.isspace())
  return strio.getvalue()

@app.route("/v/<title>/<int:vol>/<fname>")
def v_fname(title: str, vol: int, fname: str):
  path = database.docsDB[title]["path"]
  vol  = database.docsDB[title]["vols"][vol - 1]
  return flask.send_from_directory(database.view_root, Path(path, vol, fname))



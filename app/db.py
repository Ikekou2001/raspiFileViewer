import json
import mimetypes
from pathlib import Path

class Obj:
  def __init__(self, **kwds):
    for k, v in kwds.items():
      if hasattr(self, k):
        setattr(self, k, v)

class Img(Obj):
  src: str = None
  alt: str = None

class View(Obj):
  title: str = None
  seq_img: list[Img] = None

class Link(Obj):
  href: str = None
  name: str = None
  type: str = None
  thumbnail: Img = None

class List(Obj):
  title: str = None
  lst: list[Link] = None

class DB:

  def __init__(self, app_static_folder: str):
    directory = Path(app_static_folder)
    self.view_root = directory / "view"
    self.file_root = directory / "file"
    self.docsDB: dict[str, dict[str, str | list[str]]] = json.load(
      open(Path(__file__).parent / "db/docs.json")
    )

  def view(self, __title: str, __vol: int) -> View:
    ret = View(title = __title)
    path = self.docsDB[__title]["path"]
    vol  = self.docsDB[__title]["vols"][__vol - 1]
    
    ret.seq_img = []
    for elm in self.view_root.joinpath(path, vol).iterdir():
      img = Img()
      img.src = f"/v/{path}/{__vol}/{elm.name}"
      img.alt = elm.stem
      ret.seq_img.append(img)

    return ret

  def list(self, __title: str) -> List:
    l = List()
    if __title == None:
      l.title = "ALL"
      l.lst = []
      for title in self.docsDB.keys():
        link = Link()
        link.name = title
        link.href = f"/l/{title}"
        l.lst.append(link)
    else:
      vols = self.docsDB[__title]["vols"]
      l.title = __title
      l.lst = []
      for i, v in enumerate(vols, 1):
        link = Link()
        link.name = __title if v == "" else v
        link.href = f"/v/{__title}/{i}"
        l.lst.append(link)
    return l

  def file(self, __path: str) -> List:
    l = List()
    path = Path(__path)
    ref = self.file_root / path
    l.title = path.name
    if not ref.exists():
      return l
    for elm in ref.iterdir():
      link = Link()
      link.href = f"/f/{path}/{elm.name}"
      link.name = str(elm.name)
      if elm.is_dir():
        link.type = "folder"
      else:
        (mtype, ext), encode = mimetypes.guess_type(elm)
        link.type = mtype
      l.lst.append(link)
    return l
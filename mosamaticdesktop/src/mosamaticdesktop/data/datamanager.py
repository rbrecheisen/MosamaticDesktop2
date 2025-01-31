import os

from mosamaticdesktop.data.session import Session
from mosamaticdesktop.data.fileset import FileSet
from mosamaticdesktop.data.models.filesetmodel import FileSetModel
from mosamaticdesktop.data.file import File
from mosamaticdesktop.data.models.filemodel import FileModel
from mosamaticdesktop.singleton import singleton


@singleton
class DataManager:
    def __init__(self) -> None:
        pass

    def create_file(self, file_path: str) -> FileSet:
        with Session() as session:
            fileset_path = os.path.split(file_path)[0]
            fileset_name = fileset_path.split(os.path.sep)[-1]
            fileset_model = FileSetModel(name=fileset_name, path=fileset_path)
            session.add(fileset_model)
            file_name = os.path.split(file_path)[1]
            file_model = FileModel(name=file_name, path=file_path, fileset_model=fileset_model)
            session.add(file_model)
            session.commit()
            fileset = FileSet(model=fileset_model)
        return fileset

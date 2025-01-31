from typing import List

from mosamaticdesktop.data.models.filesetmodel import FileSetModel
from mosamaticdesktop.data.file import File


class FileSet:
    def __init__(self, model: FileSetModel) -> None:
        self._id = model.id
        self._name = model.name
        self._path = model.path
        
        self._files = []
        for file_model in model.file_models:
            file = File(model=file_model)
            self._files.append(file)

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name
    
    def set_name(self, name: str) -> None:
        self._name = name
    
    def path(self) -> str:
        return self._path
    
    def add_file(self, file: File) -> None:
        self._files.append(file)

    def files(self) -> List[File]:
        return self._files

    def nr_files(self) -> int:
        return len(self._files)
from enum import Enum

from mosamaticdesktop.tasks.copyfilestask import CopyFilesTask
from mosamaticdesktop.tasks.copyfilestaskdialog import CopyFilesTaskDialog


class TaskRegistry(Enum):
    COPY_FILES = (CopyFilesTask, CopyFilesTaskDialog)
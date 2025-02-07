from mosamaticdesktop.tasks.copyfilestask import CopyFilesTask
from mosamaticdesktop.tasks.copyfilestaskdialog import CopyFilesTaskDialog

TASK_REGISTRY = {
    'CopyFilesTask': (CopyFilesTask, CopyFilesTaskDialog)
}
from mosamaticdesktop.tasks.copyfilestask import CopyFilesTask
from mosamaticdesktop.tasks.copyfilestaskdialog import CopyFilesTaskDialog
from mosamaticdesktop.tasks.copydicomfilestask import CopyDicomFilesTask
from mosamaticdesktop.tasks.copydicomfilestaskdialog import CopyDicomFilesTaskDialog
from mosamaticdesktop.tasks.musclefatsegmentationtask import MuscleFatSegmentationTask
from mosamaticdesktop.tasks.musclefatsegmentationtaskdialog import MuscleFatSegmentationTaskDialog


TASK_REGISTRY = {
    'CopyFilesTask': (CopyFilesTask, CopyFilesTaskDialog),
    'CopyDicomFilesTask': (CopyDicomFilesTask, CopyDicomFilesTaskDialog),
    'MuscleFatSegmentationTask': (MuscleFatSegmentationTask, MuscleFatSegmentationTaskDialog),
}
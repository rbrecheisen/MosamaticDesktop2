from mosamaticdesktop.tasks.copyfilestask import CopyFilesTask
from mosamaticdesktop.tasks.copyfilestaskdialog import CopyFilesTaskDialog
from mosamaticdesktop.tasks.copydicomfilestask import CopyDicomFilesTask
from mosamaticdesktop.tasks.copydicomfilestaskdialog import CopyDicomFilesTaskDialog
from mosamaticdesktop.tasks.rescaledicomfilestask import RescaleDicomFilesTask
from mosamaticdesktop.tasks.rescaledicomfilestaskdialog import RescaleDicomFilesTaskDialog
from mosamaticdesktop.tasks.musclefatsegmentationtask import MuscleFatSegmentationTask
from mosamaticdesktop.tasks.musclefatsegmentationtaskdialog import MuscleFatSegmentationTaskDialog


TASK_REGISTRY = {
    'CopyFilesTask': (CopyFilesTask, CopyFilesTaskDialog),
    'CopyDicomFilesTask': (CopyDicomFilesTask, CopyDicomFilesTaskDialog),
    'RescaleDicomFilesTask': (RescaleDicomFilesTask, RescaleDicomFilesTaskDialog),
    'MuscleFatSegmentationTask': (MuscleFatSegmentationTask, MuscleFatSegmentationTaskDialog),
}
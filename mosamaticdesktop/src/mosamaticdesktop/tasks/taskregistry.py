from mosamaticdesktop.tasks.copyfilestask import CopyFilesTask
from mosamaticdesktop.tasks.copyfilestaskdialog import CopyFilesTaskDialog
from mosamaticdesktop.tasks.decompressdicomfilestask import DecompressDicomFilesTask
from mosamaticdesktop.tasks.decompressdicomfilestaskdialog import DecompressDicomFilesTaskDialog
from mosamaticdesktop.tasks.rescaledicomfilestask import RescaleDicomFilesTask
from mosamaticdesktop.tasks.rescaledicomfilestaskdialog import RescaleDicomFilesTaskDialog
from mosamaticdesktop.tasks.musclefatsegmentationtask import MuscleFatSegmentationTask
from mosamaticdesktop.tasks.musclefatsegmentationtaskdialog import MuscleFatSegmentationTaskDialog
from mosamaticdesktop.tasks.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask
from mosamaticdesktop.tasks.createpngsfromsegmentationstaskdialog import CreatePngsFromSegmentationsTaskDialog


TASK_REGISTRY = {
    'CopyFilesTask': (CopyFilesTask, CopyFilesTaskDialog),
    'DecompressDicomFilesTask': (DecompressDicomFilesTask, DecompressDicomFilesTaskDialog),
    'RescaleDicomFilesTask': (RescaleDicomFilesTask, RescaleDicomFilesTaskDialog),
    'MuscleFatSegmentationTask': (MuscleFatSegmentationTask, MuscleFatSegmentationTaskDialog),
    'CreatePngsFromSegmentationsTask': (CreatePngsFromSegmentationsTask, CreatePngsFromSegmentationsTaskDialog),
}
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
from mosamaticdesktop.tasks.calculatemetricstask import CalculateMetricsTask
from mosamaticdesktop.tasks.calculatemetricstaskdialog import CalculateMetricsTaskDialog


TASK_REGISTRY = {

    'CopyFilesTask': (
        CopyFilesTask, 
        CopyFilesTaskDialog, """
CopyFilesTask
=============
Copies files without modification from the input directory to its output directory.

Parameters: None
"""),

    
    'DecompressDicomFilesTask': (
        DecompressDicomFilesTask, 
        DecompressDicomFilesTaskDialog, """
DecompressDicomFilesTask
========================
Loads DICOM images from the input directory and checks if they are JPEG2000 compressed. If they are, the
DICOM files will be decompressed and saved to the output directory. If not, they will be copied without
modification to the output directory.

Parameters: None
"""),

    
    'RescaleDicomFilesTask': (
        RescaleDicomFilesTask, 
        RescaleDicomFilesTaskDialog, """
RescaleDicomFilesTask
=====================
Rescales DICOM files to 512 x 512 if needed. If files are rescaled 
their file names will be written to an output file 'rescaled_files.txt' 
and the rescaled files will be saved in the output directory. If no rescaling
is needed, they will be copied without modification to the output directory.

Parameters:
 - Target image size: Number of pixels in both rows and columns of the image.
"""),

    
    'MuscleFatSegmentationTask': (
        MuscleFatSegmentationTask, 
        MuscleFatSegmentationTaskDialog, """
MuscleFatSegmentationTask
=========================
Runs automatic segmentation of muscle and fat on the DICOM images. Requires
loading the AI model files in the task parameters dialog. 

Parameters:
 - Model directory: Directory containing PyTorch model files.
"""),

    
    'CreatePngsFromSegmentationsTask': (
        CreatePngsFromSegmentationsTask, 
        CreatePngsFromSegmentationsTaskDialog, """
CreatePngsFromSegmentationTask
==============================
Creates PNG images of segmentation files created by MuscleFatSegmentationTask. 

Parameters:
 - Figure width: Width of the figure (default: 10).
 - Figure height: Height of the figure (default: 10).
"""),

    
    'CalculateMetricsTask': (
        CalculateMetricsTask, 
        CalculateMetricsTaskDialog, """
CalculateMetricsTask
====================
Calculate a number of body composition metrics from the muscle and fat regions
segmented by the MuscleFatSegmentationTask. Requires loading of the original 
DICOM images as well, probably the output images of the DecompressDicomFilesTask or
RescaleDicomFilesTask. These images can be loaded in the task parameters dialog.

Parameters: 
 - Image directory: Directory containing original images (possibly rescaled).
 - Patient heights: CSV file containing patient heights.
"""),
}
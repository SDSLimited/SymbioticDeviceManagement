#!/usr/bin/env python3

'''

utilities.data.py

Copyright (C) 2023, Sustainable Drainage Systems (SDS) Limited
Technology Systems Directorate

'''

# ----------------------------------------------------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------------------------------------------------

from config import *  # Dependency, logging and configuration management.

# ----------------------------------------------------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------------------------------------------------

dataLogger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------------------------------------------------


def cleanupLogDirectory():

    functionName = 'cleanupLogDirectory'

    '''
    -- Description

    -- Arguments

    -- Retruns

    '''

    exitState = False  # Return variables.

    # -------------------------------------------------- Main ----------------------------------------------------------

    try:
        dataLogger.debug('{},Checking if log directory cleanup is required.'.format(functionName))

        archiveDir = logDir / 'archive'

        cleanupRequired = False
        if (datetime.now().day == 1):  # Check if a cleanup is required. Cleanup on 1st of Month.
            if os.path.exists(archiveDir):  # If archive directory already exists.
                # Check if the archive directory was modified today i.e. has the directory already been cleaned up.
                archiveModificationTime = datetime.utcfromtimestamp(archiveDir.stat().st_mtime)
                archiveModificationTime = archiveModificationTime.replace(hour=0, minute=0, second=0, microsecond=0)
                if (archiveModificationTime != datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)):
                    cleanupRequired = True
                    dataLogger.debug('{},Log directory cleanup is required. Trigger: First day of month and archive '
                                     'directory has not been updated today.'.format(functionName))
            else:  # Directory doesn't exist so cleanup is required.
                cleanupRequired = True
                dataLogger.debug('{},Log directory cleanup is required. Trigger: First day of month and archive '
                                 'directory does not exist.'.format(functionName))

        if cleanupRequired:  # Cleanup process. All directories older than threshold zip and moved to archive.
            archiveDir.mkdir(parents=True, exist_ok=True)  # Generate directory if not already present.
            cleanupTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # Generate filepath for zipped files.
            tarFilepath = archiveDir / (cleanupTime + '.tgz')
            dataLogger.debug('{},Archiving log files older than threshold ({} seconds) to tar file: {}.'
                             .format(functionName, logFileAgeLimit, tarFilepath))
            with tarfile.open(tarFilepath, 'w:gz') as tar:
                for path in os.listdir(str(logDir)):
                    if (path != 'archive'):
                        filepath = logDir / path
                        filepathModificationTime = datetime.utcfromtimestamp(filepath.stat().st_mtime)
                        filepathAge = (datetime.now() - filepathModificationTime).total_seconds()
                        if (filepathAge >= logFileAgeLimit):
                            dataLogger.debug('{},File added to tar file. Filepath: {}. Age: {} seconds'
                                             .format(functionName, filepath, filepathAge))
                            tar.add(filepath)
                            dataLogger.debug('{},Deleting file. Filepath: {}.'.format(functionName, filepath))
                            os.remove(filepath)

        exitState = True
    except:
        dataLogger.exception('{},Unhandled Exception!'.format(functionName))

    # ------------------------------------------------- Returns --------------------------------------------------------

    return exitState

    # --------------------------------------------------- End ----------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------

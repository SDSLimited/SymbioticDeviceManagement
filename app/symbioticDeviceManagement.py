#!/usr/bin/env python3

'''

symbioticDeviceManagement.py

Copyright (C) 2023, Sustainable Drainage Systems (SDS) Limited
Technology Systems Directorate

'''

# ----------------------------------------------------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------------------------------------------------

from config import *  # Dependency, logging and configuration management.

from utilities import data
from utilities import symbiotic
from utilities import connectivity

# ----------------------------------------------------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------------------------------------------------

applicationLogger = logging.getLogger('symbioticDeviceManagement')
applicationLogger.info('Application invoked.')

# ----------------------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------------------

print('----- SYMBiotIC Device Management -----')
print('')
print('This application will allow you to publish device shadow updates to target devices in SYMBiotIC. Please')
print('define the device shadow update message you wish to issue through the following inputs.')
print('')
print('-----')

# ---------- Inputs
applicationLogger.info('')
applicationLogger.info('Operational Inputs: ')

targetEnvironment = 'Production'
targetAction = '2'
targetValue = '20.00'
targetUnits = 'L'
targetValidFromTime = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
targetValidToTime = targetValidFromTime + timedelta(hours=2)
targetMethod = '1'
targetAdditional = 'None'
targetDevices = ['d-7cda64a5']

applicationLogger.info('Target SYMBiotIC Environment: {}.'.format(targetEnvironment))
applicationLogger.info('Target SYMBiotIC Action Type: {}.'.format(targetAction))
applicationLogger.info('Target Value: {}.'.format(targetValue))
applicationLogger.info('Target Units: {}.'.format(targetUnits))
applicationLogger.info('Target Valid From Time: {}.'.format(targetValidFromTime))
applicationLogger.info('Target Valid To Time: {}.'.format(targetValidToTime))
applicationLogger.info('Target Method: {}.'.format(targetMethod))
applicationLogger.info('Target Additional Information: {}.'.format(targetAdditional))
applicationLogger.info('Target Device Count: {} Devices.'.format(len(targetDevices)))
applicationLogger.info('Target Devices: {}.'.format(targetDevices))

# -----

applicationLogger.info('')

# ----------

applicationLogger.info('Application paused until internet connection is confirmed.')
if connectivity.waitForInternetConnection():
    applicationLogger.info('Connecting to SYMBiotIC AWS {} environment.'.format(targetEnvironment))
    if symbiotic.configAWSConnection(environment=targetEnvironment):
        applicationLogger.info('Publishing device shadow update to {} devices.'.format(len(targetDevices)))
        for targetDeviceID in targetDevices:
            applicationLogger.info('----------')
            applicationLogger.info('SYMBiotIC Device ID: {}.'.format(targetDeviceID))
            applicationLogger.info('Generating JSON document.')
            shadowDoc, shadowDocOK = symbiotic.generateShadowJSONDocument(targetAction,
                                                                          targetValue,
                                                                          targetUnits,
                                                                          targetValidFromTime,
                                                                          targetValidToTime,
                                                                          targetMethod,
                                                                          targetAdditional)
            if shadowDocOK:
                applicationLogger.info('Publishing update to device shadow.')
                if symbiotic.publishJSONDocument(targetDeviceID, shadowDoc, jsonDocumentType='Shadow'):
                    applicationLogger.info('Update published successfully.')
            applicationLogger.info('----------')

    applicationLogger.info('Disconnecting from SYMBiotIC AWS {} environment.'.format(targetEnvironment))
    symbiotic.configAWSConnection(connectionState='Disconnect')

    applicationLogger.info('Cleaning up log directory')
    data.cleanupLogDirectory()

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------

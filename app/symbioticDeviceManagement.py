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

# ---------- User Inputs

applicationLogger.info('Gathering user inputs for device shadow update.')
applicationLogger.info('')
applicationLogger.info('User Inputs: ')

# ----- Environment

print('')
print('Current SYMBiotIC environments: ')
print('Staging')
print('Production')
print('')

environments = ['Staging', 'Production']
targetEnvironment = 'Staging'
validInput = False
while True:
    environmentInput = input('Please specify the SYMBiotIC environment you wish to work in: ')
    environmentInput = environmentInput.strip()
    for environment in environments:
        if (environmentInput.casefold() == environment.casefold()):
            applicationLogger.info('Target SYMBiotIC Environment: {}.'.format(environment))
            targetEnvironment = environment
            validInput = True
            break
    if (not validInput):
        print('The SYMBiotic environment entered was not valid, please try again.')
    else:
        break

# -----

# ----- Action Type

print('')
print('Current SYMBiotIC action types (Action Code - Action): ')
print('1 - Actuate Valve or Other Actuator.')
print('10 - Terminate Existing Actions and Clear All Extant Device Shadow Updates.')
print('20 - Configuration Update - Add/Amend "tankOnStand" Variable.')
print('21 - Configuration Update - Add/Amend "temporaryOTAURL" variable.')
print('22 - Configuration Update - Add/Amend "inlinePressureTransducer" variable.')
print('')

actions = ['1', '10', '20', '21', '22']
targetAction = '1'
validInput = False
while True:
    actionInput = input('Please specify the SYMBiotIC action type you wish to execute: ')
    actionInput = actionInput.strip()
    if (actionInput not in actions):
        print('The SYMBiotIC action type was not valid, please try again.')
    else:
        applicationLogger.info('Target SYMBiotIC Action Type: {}.'.format(actionInput))
        targetAction = actionInput
        validInput = True
        break

# -----

# ----- Value

values = ['0.00', '1.00']
targetValue = '1.00'
validInput = False
if (targetAction == '1'):

    print('')
    print('Current valve or actuator actions are controlled by a target water depth with the following limits: ')
    print('Miniumum - 0.00 M')
    print('Maximum - 2.00 M')
    print('')

    while True:
        valueInput = input('Please specify a target water depth for this actuation: ')
        valueInput = valueInput.strip()
        if (0.00 < float(valueInput) <= 2.00):
            applicationLogger.info('Target Value: {}.'.format(valueInput))
            targetValue = valueInput
            validInput = True
            break
        else:
            print('The target water depth you specified was not valid, please try again.')
elif (targetAction == '10'):
    applicationLogger.info('Target Value: {}.'.format(targetValue))
elif (targetAction == '20'):

    print('')
    print('The "tankOnStand" configuration variable can be set with the following values: ')
    print('Tank Not on Stand - 0.00')
    print('Tank is on Stand - 1.00')
    print('')

    while True:
        valueInput = input('Please specify the value you wish the "tankOnStand" variable to be set to: ')
        valueInput = valueInput.strip()
        if (valueInput not in values):
            print('The value you specified was not valid, please try again.')
        else:
            applicationLogger.info('Target Value: {}.'.format(valueInput))
            targetValue = valueInput
            validInput = True
            break
elif (targetAction == '21'):
    applicationLogger.info('Target Value: {}.'.format(targetValue))
elif (targetAction == '22'):

    print('')
    print('The "inlinePressureTransducer" configuration variable can be set with the following values: ')
    print('Inline Pressure Transducer Not Present - 0.00')
    print('Inline Pressure Transducer Present - 1.00')
    print('')

    while True:
        valueInput = input('Please specify the value you wish the "inlinePressureTransducer" variable to be set to: ')
        valueInput = valueInput.strip()
        if (valueInput not in values):
            print('The value you specified was not valid, please try again.')
        else:
            applicationLogger.info('Target Value: {}.'.format(valueInput))
            targetValue = valueInput
            validInput = True
            break

# -----

# ----- Units

targetUnits = 'M'
applicationLogger.info('Target Units: {}.'.format(targetUnits))

# -----

# ----- Validity Period

targetValidFromTime = datetime.now().replace(minute=0, second=0, microsecond=0)
validInput = False

print('')
print('Current SYMBiotIC shadow updates are valid for a set period of time, in which the edge device can subscribe to')
print('and action the update. This period of time can vary, generally between 1 and 24 hours: ')
print('Minimum Validity Period - 1 Hour')
print('Maximum Validity period - 24 Hours')
print('')

while True:
    validityInput = input('Please specify a period of validity for this update: ')
    validityInput = validityInput.strip()
    if (1 <= int(validityInput) <= 24):
        applicationLogger.info('Target Validity Period: {} Hours.'.format(validityInput))
        targetValidToTime = targetValidFromTime + timedelta(hours=int(validityInput))
        validInput = True
        break
    else:
        print('The validity period you specified was not valid, please try again.')

applicationLogger.info('Target Valid From Time: {}.'.format(targetValidFromTime))
applicationLogger.info('Target Valid To Time: {}.'.format(targetValidToTime))

# -----

# ----- Method

targetMethod = '1'
applicationLogger.info('Target Method: {}.'.format(targetMethod))

# -----

# ----- Additional

targetAdditional = 'None'
validInput = False

if (targetAction == '21'):

    print('')
    print('The "temporaryOTAURL" variable can be used to trigger firmware updates via a specific URL. Note that this')
    print('variable cannot be validated, so ensure it is correct when you enter it.')
    print('')

    additionalInput = input('Please specify a valid OTA Update manifest URL: ')
    additionalInput = additionalInput.strip()
    applicationLogger.info('Target Additional Information: {}.'.format(additionalInput))
    targetAdditional = additionalInput
    validInput = True

# -----

# ----- Device ID's

print('')
print('The device shadow update can be sent to one or more device in the given SYMBiotIC environment, Devices cannot')
print('be validated so ensure they are correct when you enter them.')
print('')

devicesInput = input('Please provide a list (comma seperated) of SYMBiotIC device IDs: ')
targetDevices = devicesInput.split(",")
targetDevices = [device.strip() for device in targetDevices]
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
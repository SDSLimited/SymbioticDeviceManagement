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
print('1 - Actuate Valve or Other Release Mechanism.')
print('2 - Trigger Irrigation Event')
print('10 - Terminate Existing Actions and Clear All Extant Device Shadow Updates.')
print('20 - Configuration Update')
print('')

actions = ['1', '2', '10', '20']
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
elif (targetAction == '2'):

    print('')
    print('Current irrigation events are controlled by a target release volume with the following limits: ')
    print('Miniumum - 0.00 Litres')
    print('Maximum - 1000.00 Litres')
    print('')

    while True:
        valueInput = input('Please specify a target release volume for this irrigation event: ')
        valueInput = valueInput.strip()
        if (0.00 < float(valueInput) <= 1000.00):
            applicationLogger.info('Target Value: {}.'.format(valueInput))
            targetValue = valueInput
            validInput = True
            break
        else:
            print('The target release volume you specified was not valid, please try again.')
elif (targetAction == '10'):
    applicationLogger.info('Target Value: {}.'.format(targetValue))
elif (targetAction == '20'):
    applicationLogger.info('Target Value: {}.'.format(targetValue))

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

if (targetAction == '2'):
    targetUnits = 'L'

applicationLogger.info('Target Units: {}.'.format(targetUnits))

# -----

# ----- Validity Period

targetValidFromTime = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
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

keys = range(0, 30, 1)
targetAdditional = 'None'
validInput = False

if (targetAction == '20'):

    print('')
    print('Configuration variables are defined in the embedded software configuration file (config.json) as key-value')
    print('pairs. The values for these variables you enter are not validated by this program, so ensure they are')
    print('when entered.')
    print('')
    print('Current SymbioticESP32 Configuration Variables: ')
    print('0 - "id"')
    print('1 - "apn"')
    print('2 - "endpoint"')
    print('3 - "OTAURL"')
    print('4 - "softwareVersionChannel" - Default: "IEmSoVn"')
    print('5 - "softwareMajorVersionChannel" - Default: "IEmSoVnMj"')
    print('6 - "softwareMinorVersionChannel" - Default: "IEmSoVnMi"')
    print('7 - "softwarePatchVersionChannel" - Default: "IEmSoVnPa"')
    print('8 - "heapMemoryChannel" - Default: "IFrHpBy"')
    print('9 - "programCounterChannel" - Default: "IMnPrCo"')
    print('10 - "signalQualityChannel" - Default: "IMoSLDb"')
    print('11 - "batteryVoltageChannel" - Default: "ISuVoVo"')
    print('12 - "batteryCurrentChannel"  - Default: "ISuCumA"')
    print('13 - "solarVoltageChannel" - Default: "OFF"')
    print('14 - "solarCurrentChannel" - Default: "OFF"')
    print('15 - "interiorTemperatureChannel" - Default: "IEnTmDC"')
    print('16 - "interiorHumidityChannel" - Default: "IEnHmPc"')
    print('17 - "actuationStateChannel" - Default: "EAcSt"')
    print('18 - "subscriptionActuationStateChannel" - Default: "ESuAcSt"')
    print('19 - "actionItemCountChannel" - Default: "IRACoCo"')
    print('20 - "releaseTargetChannel" - Default: "EWaTaM"')
    print('21 - "irrigationTargetChannel" - Default: "EIrTaL"')
    print('22 - "irrigationSupplyChannel" - Default: "ERWTrL"')
    print('23 - "onewireBChannel" - Default: "EArTmDC"')
    print('24 - "pulseCountAChannel" - Default: "EFMFlL"')
    print('25 - "pulseCountBChannel" - Default: "EFMAFIL"')
    print('26 - "analogueSensorAChannel" - Default: "EWaDeMe"')
    print('27 - "analogueSensorBChannel" - Default: "OFF"')
    print('28 - "analogueSensorCChannel" - Default: "EVSVoVo"')
    print('29 - "4to20mACalibrationMinimum" - Default: "0.00"')
    print('30 - "4to20mACalibrationMaximum" - Default: "2.00"')
    print('')

while True:
    configKeyInput = input('Please specify the SYMBiotIC configuration variable key you wish to update (0-30): ')
    configKeyInput = configKeyInput.strip()
    if (configKeyInput not in keys):
        print('The SYMBiotIC configuration variable key was not valid, please try again.')
    else:
        validInput = True
        break

print('')
print('Please specify the value you wish to set SYMBiotIC configuration variable to. Note that "OFF" for a channel ')
configValueInput = input('variable will stop that sensor/channel being sampled: ')

configurationVariableKey = 'None'
configurationVariableValue = configValueInput

if (configKeyInput == '0'):
    configurationVariableKey = 'id'




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

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
print('20 - Configuration Update - Add or Ammend Configuration Variables')
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

# ----- Method

targetMethod = '1'
applicationLogger.info('Target Method: {}.'.format(targetMethod))

# -----

# ----- Value

targetValue = '1.00'
validInput = False
if (targetAction == '1'):

    print('')
    print('Current valve or actuator actions are controlled by a target water depth with the following limits: ')
    print('Miniumum - -2.00 M')
    print('Maximum - 2.00 M')
    print('NB: Negative values indicate a relative depth change. So -0.2 M will release to 0.2 M below the current ')
    print('level. Positive values will release to an absolute target depth. So 0.3 M will drain the tank to 0.3 M.')
    print('')

    while True:
        valueInput = input('Please specify a target water depth for this actuation: ')
        valueInput = valueInput.strip()
        if (-2.00 < float(valueInput) <= 2.00):
            applicationLogger.info('Target Value: {}.'.format(valueInput))
            targetValue = valueInput
            validInput = True
            if (float(targetValue) < 0.00):
                targetMethod = '2'
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

# ----- Additional

options = ['0', '1']
keys = range(0, 32, 1)
targetAdditional = 'None'
configurationVariableKey = 'None'
configurationVariableValue = 'None'
validInput = False

if (targetAction == '20'):

    print('')
    print('Current options for SYMBiotICESP32 configuration variable updates: ')
    print('0 - Update/Ammend Existing Configuration variable')
    print('1 - Add New Configuration Variable')
    print('')

    while True:
        optionInput = input('Please the option you wish to use for configuration variable updates: ')
        optionInput = optionInput.strip()
        if (optionInput not in options):
            print('The option selected was not valid, please try again.')
        else:
            validInput = True
            break

    if (optionInput == '0'):

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
        print('31 - "TemporaryOTAURL"')
        print('')

        while True:
            configKeyInput = input('Please specify the SYMBiotIC configuration variable key you wish to update (0-31): ')
            configKeyInput = configKeyInput.strip()
            if (int(configKeyInput) not in keys):
                print('The SYMBiotIC configuration variable key was not valid, please try again.')
            else:
                validInput = True
                break

        print('')
        print('Please specify the value you wish to set SYMBiotIC configuration variable to. Note that "OFF" for a ')
        configValueInput = input('channel variable will stop that sensor/channel being sampled: ')

        configurationVariableValue = configValueInput

        if (configKeyInput == '0'):
            configurationVariableKey = 'id'
        elif (configKeyInput == '1'):
            configurationVariableKey = 'apn'
        elif (configKeyInput == '2'):
            configurationVariableKey = 'endpoint'
        elif (configKeyInput == '3'):
            configurationVariableKey = 'OTAURL'
        elif (configKeyInput == '4'):
            configurationVariableKey = 'softwareVersionChannel'
        elif (configKeyInput == '5'):
            configurationVariableKey = 'softwareMajorVersionChannel'
        elif (configKeyInput == '6'):
            configurationVariableKey = 'softwareMinorVersionChannel'
        elif (configKeyInput == '7'):
            configurationVariableKey = 'softwarePatchVersionChannel'
        elif (configKeyInput == '8'):
            configurationVariableKey = 'heapMemoryChannel'
        elif (configKeyInput == '9'):
            configurationVariableKey = 'programCounterChannel'
        elif (configKeyInput == '10'):
            configurationVariableKey = 'signalQualityChannel'
        elif (configKeyInput == '11'):
            configurationVariableKey = 'batteryVoltageChannel'
        elif (configKeyInput == '12'):
            configurationVariableKey = 'batteryCurrentChannel'
        elif (configKeyInput == '13'):
            configurationVariableKey = 'solarVoltageChannel'
        elif (configKeyInput == '14'):
            configurationVariableKey = 'solarCurrentChannel'
        elif (configKeyInput == '15'):
            configurationVariableKey = 'interiorTemperatureChannel'
        elif (configKeyInput == '16'):
            configurationVariableKey = 'interiorHumidityChannel'
        elif (configKeyInput == '17'):
            configurationVariableKey = 'actuationStateChannel'
        elif (configKeyInput == '18'):
            configurationVariableKey = 'subscriptionActuationStateChannel'
        elif (configKeyInput == '19'):
            configurationVariableKey = 'actionItemCountChannel'
        elif (configKeyInput == '20'):
            configurationVariableKey = 'releaseTargetChannel'
        elif (configKeyInput == '21'):
            configurationVariableKey = 'irrigationTargetChannel'
        elif (configKeyInput == '22'):
            configurationVariableKey = 'irrigationSupplyChannel'
        elif (configKeyInput == '23'):
            configurationVariableKey = 'onewireBChannel'
        elif (configKeyInput == '24'):
            configurationVariableKey = 'pulseCountAChannel'
        elif (configKeyInput == '25'):
            configurationVariableKey = 'pulseCountBChannel'
        elif (configKeyInput == '26'):
            configurationVariableKey = 'analogueSensorAChannel'
        elif (configKeyInput == '27'):
            configurationVariableKey = 'analogueSensorBChannel'
        elif (configKeyInput == '28'):
            configurationVariableKey = 'analogueSensorCChannel'
        elif (configKeyInput == '29'):
            configurationVariableKey = '4to20mACalibrationMinimum'
        elif (configKeyInput == '30'):
            configurationVariableKey = '4to20mACalibrationMaximum'
        elif (configKeyInput == '31'):
            configurationVariableKey = 'TemporaryOTAURL'

    elif (optionInput == '1'):

        print('')
        print('Configuration variables are defined in the embedded software configuration file (config.json) as key-value')
        print('pairs. To define a new configuration variable, you will need to specify a key and value. Obviously ')
        print('these values cannot be validated so take care when entering them.')
        print('')

        configKeyInput = input('Please specify the SYMBiotIC configuration variable key you wish to create: ')
        configKeyInput = configKeyInput.strip()

        configValueInput = input('Please specify the SYMBiotIC configuration variable value you wish to create: ')
        configValueInput = configValueInput.strip()

        configurationVariableKey = configKeyInput
        configurationVariableValue = configValueInput

    targetAdditional = ('{},{}'.format(configurationVariableKey, configurationVariableValue))
    applicationLogger.info('Target Additional {}.'.format(targetAdditional))
else:
    applicationLogger.info('Target Additional {}.'.format(targetAdditional))

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

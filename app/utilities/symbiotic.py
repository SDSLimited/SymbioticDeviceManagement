#!/usr/bin/env python3

'''

utilities.symbiotic.py

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

symbioticLogger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
# Globals
# ----------------------------------------------------------------------------------------------------------------------

symbioticMQTTClient = []

# ----------------------------------------------------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------------------------------------------------


def configAWSConnection(environment='Production', connectionState='Connect'):

    functionName = 'configAWSConnection'

    '''
    -- Description

    -- Arguments

    -- Retruns

    '''

    exitState = False  # Return variables.

    # --------------------------------------------------- Main ---------------------------------------------------------

    try:
        global symbioticMQTTClient
        if (connectionState == 'Connect'):
            if (environment == 'Staging'):
                for attempt in range(requestAttempts):
                    # Configure MQTT client according to settings in the configuration script and this devices unique
                    # device ID and AWS certificates, then intialise a connection.
                    try:
                        symbioticMQTTClient = AWSIoTMQTTClient(stagingDeviceID)
                        symbioticMQTTClient.configureEndpoint(stagingAWSEndpoint, 8883)
                        symbioticMQTTClient.configureCredentials(str(stagingAWSRootCAFilepath),
                                                                 str(stagingAWSPrivateKeyFilepath),
                                                                 str(stagingAWSCertFilepath))
                        symbioticMQTTClient.configureOfflinePublishQueueing(-1)
                        symbioticMQTTClient.configureDrainingFrequency(2)
                        symbioticMQTTClient.configureConnectDisconnectTimeout(3)
                        symbioticMQTTClient.configureMQTTOperationTimeout(5)
                        if symbioticMQTTClient.connect():
                            exitState = True
                            symbioticLogger.debug('{},Connected to AWS Staging environment successfully on attempt {} '
                                                  ' of {}. Device ID: {}. AWS Endpoint: {}.'.format(functionName,
                                                                                                    attempt+1,
                                                                                                    requestAttempts,
                                                                                                    stagingDeviceID,
                                                                                                    stagingAWSEndpoint))
                            break  # Break on successful connection to AWS.
                        else:
                            symbioticLogger.debug('{},Failed to connect to AWS Staging environment on attempt {} of {}!'
                                                  .format(functionName, attempt+1, requestAttempts))
                    except Exception as e:
                        symbioticLogger.debug('{},Failed to connect to AWS Staging environment on attempt {} of {}! '
                                              'Action caused exception. Exception: {}.'.format(functionName,
                                                                                               attempt+1,
                                                                                               requestAttempts,
                                                                                               e))
                    time.sleep(requestAttemptWait)  # Wait before next attempt.
                else:
                    symbioticLogger.critical('{},Timed out after {} attempts! Could not connect to AWS Staging '
                                             'environment.'.format(functionName, attempt+1))
            elif (environment == 'Production'):
                for attempt in range(requestAttempts):
                    # Configure MQTT client according to settings in the configuration script and this devices unique
                    # device ID and AWS certificates, then intialise a connection.
                    try:
                        symbioticMQTTClient = AWSIoTMQTTClient(productionDeviceID)
                        symbioticMQTTClient.configureEndpoint(productionAWSEndpoint, 8883)
                        symbioticMQTTClient.configureCredentials(str(productionAWSRootCAFilepath),
                                                                 str(productionAWSPrivateKeyFilepath),
                                                                 str(productionAWSCertFilepath))
                        symbioticMQTTClient.configureOfflinePublishQueueing(-1)
                        symbioticMQTTClient.configureDrainingFrequency(2)
                        symbioticMQTTClient.configureConnectDisconnectTimeout(3)
                        symbioticMQTTClient.configureMQTTOperationTimeout(5)
                        if symbioticMQTTClient.connect():
                            exitState = True
                            symbioticLogger.debug('{},Connected to AWS Production environment successfully on attempt '
                                                  '{} of {}. Device ID: {}. AWS Endpoint: {}.'
                                                  .format(functionName,
                                                          attempt+1,
                                                          requestAttempts,
                                                          productionDeviceID,
                                                          productionAWSEndpoint))
                            break  # Break on successful connection to AWS.
                        else:
                            symbioticLogger.debug('{},Failed to connect to AWS Production environment on attempt {} of '
                                                  ' {}!'.format(functionName, attempt+1, requestAttempts))
                    except Exception as e:
                        symbioticLogger.debug('{},Failed to connect to AWS Production environment on attempt {} of {}! '
                                              'Action caused exception. Exception: {}.'.format(functionName,
                                                                                               attempt+1,
                                                                                               requestAttempts,
                                                                                               e))
                    time.sleep(requestAttemptWait)  # Wait before next attempt.
                else:
                    symbioticLogger.critical('{},Timed out after {} attempts! Could not connect to AWS Production '
                                             'environment.'.format(functionName, attempt+1))
        elif (connectionState == 'Disconnect'):
            try:
                if symbioticMQTTClient.disconnect():
                    exitState = True
                    symbioticLogger.debug('{},Disconnected from AWS successfully.'.format(functionName))
                else:
                    symbioticLogger.warning('{},Failed to disconnect from AWS!'.format(functionName))
            except Exception as e:
                symbioticLogger.error('{},Failed to disconnect from AWS! Action caused exception. Exception: {}'
                                      .format(functionName, e))
        else:
            symbioticLogger.error('{},Invalid input argument! Argument: connectionState. Input: {}.'
                                  .format(functionName, connectionState))
    except:
        symbioticLogger.exception('{},Unhandled Exception!'.format(functionName))

    # -------------------------------------------------- Returns -------------------------------------------------------

    return exitState

    # ---------------------------------------------------- End ---------------------------------------------------------


def generateShadowJSONDocument(action, value, units, startTime, endTime, method, additional):

    functionName = 'generateShadowJSONDocument'

    '''
    -- Description

    -- Arguments

    -- Retruns

    '''

    exitState = False  # Return variables.
    jsonData = {}
    jsonDocument = json.dumps(jsonData)

    # --------------------------------------------------- Main ---------------------------------------------------------

    try:
        #  Generate a JSON document in the format for a device shadow update and populate it with the supplied details.
        jsonData = {'state': {'desired': {'Actions': []}}}  # Create a nested dict with the desired format.
        # Use controlDecision input list to populate the 'Actions' section in the nested dict.
        jsonData['state']['desired']['Actions'].append({
            'Action': ('{}'.format(action)),
            'Value': ('{}'.format(value)),
            'Unit': ('{}'.format(units)),
            'StartTime': ('{}'.format(startTime.strftime(AWSDateTimeFormat))),
            'EndTime': ('{}'.format(endTime.strftime(AWSDateTimeFormat))),
            'Method': ('{}'.format(method)),
            'Additional': ('{}'.format(additional))})
        # Convert dict to JSON document.
        jsonDocument = json.dumps(jsonData)

        exitState = True
        symbioticLogger.debug('{},JSON document generated succesfully.'.format(functionName))
        symbioticLogger.debug('{},JSON document: {}.'.format(functionName, jsonDocument))
    except:
        symbioticLogger.exception('{},Unhandled Exception!'.format(functionName))

    # ------------------------------------------------- Returns --------------------------------------------------------

    return jsonDocument, exitState

    # --------------------------------------------------- End ----------------------------------------------------------


def publishJSONDocument(targetDeviceID, jsonDocument, jsonDocumentType='Data', simulation=False):

    functionName = 'publishJSONDocument'

    '''
    -- Description

    -- Arguments

    -- Retruns

    '''

    exitState = False  # Return variables.

    # --------------------------------------------------- Main ---------------------------------------------------------

    try:
        global symbioticMQTTClient
        try:
            # Define AWS topic to publish to, based on JSON document type.
            if (jsonDocumentType == 'Data'):
                topic = ('ydoc-ml/{}/data/jsn'.format(targetDeviceID))
                qualityOfService = 1  # Ensure quality of service set to 1 to avoid intermitent data losses.
            elif (jsonDocumentType == 'Shadow'):
                topic = ('$aws/things/{}/shadow/update'.format(targetDeviceID))
                qualityOfService = 1  # Ensure quality of service set to 1 to avoid intermitent data losses.
            # If not in simulation mode attempt to publish JSON document to AWS, otherwise do not attempt to publish and
            # assume everything worked.
            if not simulation:
                if symbioticMQTTClient.publish(topic, jsonDocument, qualityOfService):
                    exitState = True
                    symbioticLogger.debug('{},JSON document sucesfully published to AWS.'.format(functionName))
                else:
                    symbioticLogger.warning('{},Failed to publish JSON document to AWS!'.format(functionName))
            else:
                symbioticLogger.debug('{},Simulation Mode: JSON document sucesfully published to AWS.'
                                      .format(functionName))
            symbioticLogger.debug('{},JSON document: {}.'.format(functionName, jsonDocument))
        except Exception as e:
            symbioticLogger.error('{},Error while publishing JSON document! Action caused exception. Exception: {}'
                                  .format(functionName, e))
    except:
        symbioticLogger.exception('{},Unhandled Exception!'.format(functionName))

    # ------------------------------------------------- Returns --------------------------------------------------------

    return exitState

    # --------------------------------------------------- End ----------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------

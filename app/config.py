#!/usr/bin/env python3

'''

config.py

Copyright (C) 2023, Sustainable Drainage Systems (SDS) Limited
Technology Systems Directorate

'''

# ----------------------------------------------------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------------------------------------------------

import os
import sys
import json
import time
import math
import numpy
import pandas
import shutil
import logging
import pathlib
import tarfile
import requests

from random import uniform, randint
from datetime import datetime, timedelta, timezone
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# ----------------------------------------------------------------------------------------------------------------------
# Root Directory
# ----------------------------------------------------------------------------------------------------------------------

# Windows
#appDir = pathlib.Path.cwd().parent

# Linux
#appDir = pathlib.Path.cwd()
#appDir = appDir / 'SymbioticDeviceManagement'

# AMI Linux - Amazon EC2
appDir = pathlib.Path('/home/ec2-user/symbioticDeviceManagement')

# ----------------------------------------------------------------------------------------------------------------------
# Logging Configuration
# ----------------------------------------------------------------------------------------------------------------------

logDir = appDir / 'logs'
logDir.mkdir(parents=True, exist_ok=True)

logTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
logFilepath = logDir / '{}.log'.format(logTime)  # Define log file name.

logging.basicConfig(filename=str(logFilepath),  # Configure logging module.
                    format='%(asctime)s,%(levelname)s,%(name)s,%(message)s',
                    datefmt='%d-%m-%Y-%H-%M-%S',
                    level=logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------------------
# Logging Instantiation
# ----------------------------------------------------------------------------------------------------------------------

configLogger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------------------

try:
    # SYMBiotIC AWS Device IDs
    stagingDeviceID = 'd-50c09258'
    productionDeviceID = 'd-4f83effa'

    # SYMBiotIC AWS Endpoints
    stagingAWSEndpoint = 'ao8enh8o9quvx-ats.iot.eu-west-1.amazonaws.com'
    productionAWSEndpoint = 'ai0v1585vxqmz-ats.iot.eu-west-1.amazonaws.com'

    # AWS DateTime Format
    AWSDateTimeFormat = '%y%m%d%H%M%S'

    # AWS Certificates
    certDir = appDir / 'certs'  # Path definitions.
    stagingAWSRootCAFilepath = certDir / 'staging' / 'ca.pem'
    stagingAWSCertFilepath = certDir / 'staging' / 'cert.pem'
    stagingAWSPrivateKeyFilepath = certDir / 'staging' / 'pkey.pem'
    productionAWSRootCAFilepath = certDir / 'production' / 'ca.pem'
    productionAWSCertFilepath = certDir / 'production' / 'cert.pem'
    productionAWSPrivateKeyFilepath = certDir / 'production' / 'pkey.pem'
    certsError = False
    stagingAWSCertsList = [stagingAWSRootCAFilepath, stagingAWSCertFilepath, stagingAWSPrivateKeyFilepath]
    for filepath in stagingAWSCertsList:
        if not filepath.is_file():
            certsError = True
            configLogger.critical('An AWS certificate for the Staging environment is missing! Missing certificate: {}.'
                                  .format(filepath))
    if certsError:
        raise Exception('There was a problem with the applications AWS Certificates for the Staging environment. See '
                        'log file for details.')
    certsError = False
    productionAWSCertsList = [productionAWSRootCAFilepath, productionAWSCertFilepath, productionAWSPrivateKeyFilepath]
    for filepath in productionAWSCertsList:
        if not filepath.is_file():
            certsError = True
            configLogger.critical('An AWS certificate for the Production environment is missing! Missing certificate: '
                                  ' {}.'.format(filepath))
    if certsError:
        raise Exception('There was a problem with the applications AWS Certificates for the Production environment. '
                        'See log file for details.')

    # Log File Age Limit
    logFileAgeLimit = 2592000  # In seconds - 2592000 = 30 days.

    # Internet Connectivity Variables
    connectivityTestURL = 'http://www.google.com'
    waitForInternetConnectionTimeout = 120.00
    requestAttempts = 5
    requestAttemptWait = 1.00
    requestAttemptTimeout = 2.00
except:
    configLogger.exception('Unhandled Exception!')
    raise Exception('Unhandled Exception!')

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------

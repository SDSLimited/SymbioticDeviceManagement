#!/usr/bin/env python3

'''

utilities.connectivity.py

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

connectivityLogger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------------------------------------------------


def waitForInternetConnection():

    functionName = 'waitForInternetConnection'

    '''
    -- Description

    -- Arguments

    -- Retruns

    '''

    exitState = False  # Return variables.

    # -------------------------------------------------- Main ----------------------------------------------------------

    try:
        attempt = 1
        startTime = datetime.now()
        while (datetime.now() - startTime).total_seconds() <= waitForInternetConnectionTimeout:
            try:
                response = requests.get(connectivityTestURL, timeout=requestAttemptTimeout)
                if response.status_code == 200:  # Status code 200 = succsessful request.
                    exitState = True
                    connectivityLogger.debug('{},Http request to {} successful on attempt {}. Internet connection '
                                             'available.'.format(functionName,
                                                                 connectivityTestURL,
                                                                 attempt))
                    break  # Break on successful get request.
                else:
                    connectivityLogger.debug('{},Http request to {} unsuccesful on attempt {}! Status code: {}.'
                                             .format(functionName,
                                                     connectivityTestURL,
                                                     attempt,
                                                     response.status_code))
            except Exception as e:  # requests.get raises an exception when no network interface available.
                connectivityLogger.debug('{},Http request to {} unsuccesful on attempt {}! Attempt caused exception. '
                                         'Exception: {}.'.format(functionName,
                                                                 connectivityTestURL,
                                                                 attempt,
                                                                 e))
            attempt += 1
            time.sleep(requestAttemptWait)  # Wait before next attempt.
        else:
            connectivityLogger.critical('{},Timed out after {} Seconds and {} attempts! No internet connection '
                                        'available.'.format(functionName,
                                                            waitForInternetConnectionTimeout,
                                                            attempt))
    except:
        connectivityLogger.exception('{},Unhandled Exception!'.format(functionName))

    # ------------------------------------------------- Returns --------------------------------------------------------

    return exitState

    # --------------------------------------------------- End ----------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------

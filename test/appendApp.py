#
# This file contains no tests, but rather helper function that are used throughout the tests
#
# 07.10.2016
#
# Usage: pytest main_test.py
#

import sys
import os

already_appended = False

TEST_FOLDER_NAME = "test"
APP_FOLDER_NAME = "app"


def appendApp():
    ''' This helper function appends the app folder to the sys.path array to make sure imports work correctly '''
    global already_appended
    if not already_appended:
        if not __file__:
            ValueError("__file__ wasn't set.'")

        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Search for parent until arrived at test
        while os.path.basename(current_dir) != TEST_FOLDER_NAME:
            if current_dir == os.path.dirname(current_dir):  # Top Level of filesystem reached
                FileNotFoundError("Couldn't find app directory'")
            current_dir = os.path.dirname(current_dir)  # Get the parent directory of current_dir

        # Then go to the parent one last time
        current_dir = os.path.dirname(current_dir)

        # Attach the /app to the path string
        app_dir = os.path.join(current_dir, APP_FOLDER_NAME)

        # Append the path to the sys.path array
        sys.path.append(app_dir)
        already_appended = True


appendApp()

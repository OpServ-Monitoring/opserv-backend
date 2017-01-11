---
layout: article
title:  "Contribute - Installation"
---

First of all you have to check the requirements for the system.
The software depends on a Python installation of version 3 or higer.

Usually you can check your Python version with the following command

    python -v

If the python command is not found, you may need to reinstall it.
Depending on your OS you could have two Python installation (one for version 2 and one for 3) on your system.
Simply try the following command to test that:

    python3 -v

In that case this command should return some Python version number.

If you have identified your Python installation, the next step is to install the Python dependencies.

If your Python 3 installation is executed with the python command enter the following commands:

    pip install -r app/prerequirements.txt
    pip install -r app/requirements.txt

If you used the python3 -v command use the following:

    pip3 install -r app/prerequirements.txt
    pip3 install -r app/requirements.txt

All the reuqirements are installed now

Usage
-----

If the installation succeeds, you're ready to simply clone/download this repository and launch the program:

    python app/main.py

or

    python3 app/main.py

Testing
-------

### Simple test

The testing requirements are located in the app/testrequirements.txt file and can be installed with

    pip install -r app/testrequirements.txt

To simply run all the tests, use the following command while being in the opserv-backend folder:

    pytest

All the required configuration should be done automatically by the conftest.py and pytest.ini files.

### Tests with code coverage

If you want to run the tests with test coverage use the following command

    pytest --cov=app

### Using a debugger with PyTest

Sometimes, especially when creating new tests, it is reuqired to debug them in someway or the other.
While PyTests functionality is pretty amazing and logs all stdout, it does not have any simple way to use for IDEs debugger with the tests.

The solution to this is directly starting the pytest.py with the path to the opserv-backend folder as an argument
Here is an example:

    python "PYTHONPATH/Lib/site-packages/pytest-3.0.3-py3.5.egg/pytest.py" "PATH_TO_OPSERV_BACKEND"

You have to redefine the locations depending on your workspace of course.
Also running this in the console won't give any more debugging functionality.
You have to find a way to integrate it into the debugging configurations of your IDE.

Below is the configuration used for VSCode:
As stated above, you still need to configure your pytest location for yourself.

```
        {
            "name": "Debug Tests",
            "type": "python",
            "request": "launch",
            "stopOnEntry": false,
            "pythonPath": "${config.python.pythonPath}",
            "program": "PATHTOPYTHON/Lib/site-packages/pytest-3.0.3-py3.5.egg/pytest.py",
            "args" : ["${workspaceRoot}/test"],
            "debugOptions": [
                "WaitOnAbnormalExit",
                "WaitOnNormalExit",
                "RedirectOutput"
            ]
        }
```
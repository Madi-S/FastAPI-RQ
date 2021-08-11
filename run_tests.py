import os
import pathlib
import pytest
from main import logger


logger.debug('Going to run all the tests')

os.chdir(pathlib.Path.cwd() / 'tests')

try:
    pytest.main()
except:
    logger.warning(
        'Make sure you have commented line #24 in main.py, so the tests can run properly')

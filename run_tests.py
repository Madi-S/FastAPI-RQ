import os
import pathlib
import pytest


print('GOING TO RUNNING ALL TESTS')

os.chdir(pathlib.Path.cwd() / 'tests')

pytest.main()

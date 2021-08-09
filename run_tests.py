import os
import pathlib
import pytest

print('HEELO WORLD')
os.chdir(pathlib.Path.cwd() / 'tests')

pytest.main()

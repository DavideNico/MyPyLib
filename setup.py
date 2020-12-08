from setuptools import setup
import re

VERSIONFILE="py_dgm/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name='py_dgm',
      version=verstr,
      description='Python library for the Directorate General Market Operations.',
      author='Directorate General Market Operations',
      author_email='AllMOSDivision@ecb.int',
	  url='https://bitbucket.ecb.de/projects/DGM/repos/py_dgm/browse',
      packages=[
		'py_dgm',        # a list of subpackages
	  ],
      package_data={'py_dgm/templates': ['templates/*.xml','templates/*.sql','templates/*.ora']},  # folder with static data e.g. XML headers, General TNS, ...
      install_requires=[
		'cx_oracle',
		'pandas',
		'xlwings',
		'treelib',
        'matplotlib',
        'pywin32',
		'seaborn'
		],
      include_package_data=True,
      zip_safe=False)

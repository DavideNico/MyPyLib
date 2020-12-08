# DG-M Library for Python
Nothing to see here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


## How to install it 


### Pre-requisites 


The following software must be installed (*If not installed, please raise an IT request*):
* Anaconda 
* GIT 

The following Python packages should be installed and up to date:
* conda
* pip

To check, open the *Anaconda Prompt* and type the following:

Check if PIP is up-to-date [see here](https://pip.pypa.io/en/stable/)
```
pip -V
```
Check if *conda* is up-to-date (the version should be >= 4.7.10)
```
conda info
```
If required, you can update them:
```
conda update conda
conda update pip
```
it might take several minutes..


### Installation

This Python library can be easily installed with the following command:
```
git config --global http.sslverify false

pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org git+ssh://git@bitbucket.ecb.de:7999/dgm/py_dgm.git --proxy https://ap-python-proxy:x2o7rCPYuN1JuV8H@p-gw.ecb.de:9090 --no-cache-dir

git config --global http.sslverify true
```
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

Alternatively, an automatic installer is available to DG-M users [here](P:\ECB business areas\DGM\Databases and programme files\Collateral Management\FMCO\Python library\moa_configuration\Installer\DGM-Setup.bat).

This automatic installer will create a new virtual Anaconda environment, called **DataManagement**, which will contain the following set of libraries:

* Standard data manipulation libraries - *Pandas, numpy*
* Standard interface libraries - *cx_Oracle, win32com*
* Standard data visualisation libraries - *matplotlib, seaborn*
* Internal libraries: 
	* **PY_DGM** - collection of common function for the Directorate General Market Operations
	* **DARWIN REST** - for reading from and uploading files in Darwin [here](https://bitbucket.ecb.de/projects/DARWINAPI/repos/python---darwin_rests/browse) 
* All the libraries specified in the .yml file (moa_configuration repository)


![Scheme](InfrastructureInstallerPYDGM.PNG)


### Contributing

A step by step series of examples that tell you how to get a development environment running

Setup a folder structure in your D-drive for the repository and its branch types. Start GIT Bash, e.g. press \<Windows Key>, type "GIT Bash" and hit \<enter> 
```
cd d:
mkdir repos
cd repos
mkdir feature
mkdir bugfix
mkdir master
mkdir release
mkdir hotfix
```

Work on a specific branch: \<branch name> can be found on https://bitbucket.ecb.de/projects/DGM/repos/py_dgm/branches
A branch is usually referenced by its type and name \<branch type/branch name>, e.g. feature/restructuring. <> brackets below are placeholders and must be replaced with actual values.

```

cd <branch type>
mkdir <branch name>
cd <branch name>

git init
git remote add origin https://bitbucket.ecb.de/scm/dgm/py_dgm.git
git clone ssh://git@bitbucket.ecb.de:7999/dgm/py_dgm.git -b <branch type/branch name>

cd py_dgm
(not needed if branch was created in Bitbucked and cloned in the command before) git checkout -b <branch type/branch name>
git push --set-upstream origin <branch type/branch name>
```

Now you can make changes to the files in the current directory. 

Files that have been added/amended/deleted must be added to the commit log using the following commands.
It is always best practice to add and commit change by change. USE MEANINGFUL COMMENTS! 

```
* for single files
git add <filepath/filename>

* for all files
git add .
```

Changes can be now committed. Comment is compulsery. 
```
git commit -m "Write here what you best liked about the change you have done!"
```

Finally push all commits to the BitBucket repository on the server with:
```
git push
```

## Who to contact

* **Davide Nicolini** - *Davide.Nicolini@ecb.europa.eu*
* **Marek Kosec** - *Marek.Kosec@ecb.europa.eu*


## Authors 

* **Davide Nicolini** - *Initial work* and *Contributor*
* **Lefkios Geladaris** - *Initial work*
* **Maximilian Blau** - *Contributor*
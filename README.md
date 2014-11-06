dogpound
========
A twitter-like service for animals other than birds.


Requirements
============
You will need the following to setup dogpound:
- Python 2.7
- pip
- virtualenv


Installation
============
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Development
===========
Before developing, it is important to setup a virtualenv (a virtual environment). To do so, create a new virtualenv (unless it already exists, skip this step):
```
virtualenv venv
```
Then activate it:
```
source venv/bin/activate
```

Vagrant Development
===================
To boot the development VM:
```
cd vagrant
make up
```
Shutdown the development VM:
```
cd vagrant
make halt
```

Running tests
=============
```
make test
```

Running the web app
===================
```
make run
```
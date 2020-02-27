# python-bangazon-api-template

Setup
The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/nss-cohort-36/bangazon-api-purely-magic-ecomm-sprint-1 .  
$ cd bangazon-api-purely-magic-ecomm-sprint-1 . 
$ cd bangazon . 
```
Create a virtual environment to install dependencies in and activate it:  
```sh
python -m venvBangazonEnv . 
source ./BangazonEnv/bin/activate (if windows based replace bin with Scripts) . 
```
Then install the dependencies:  
```sh
(env)$ pip install -r requirements.txt . 
```
Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by . 

Once pip has finished downloading the dependencies:  
```sh
(env)$ cd project . 
(env)$ python manage.py runserver . 
```
And navigate to http://127.0.0.1:8000.  

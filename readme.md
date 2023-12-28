# Accounts API Project
### API to manage users and accounts. Developed using Django & Django Rest Framework.

## Getting started

Required Python 3.11 or later

### Clone repository
First you will need to clone down the repository.

1) Create a new directory on your computer. This will be the 'root directory'.

2) Open a terminal and cd into the root directory.

3) You can now clone the project from GitHub. You can do this a few different ways.
I use HTTPS.
```
- git clone https://github.com/danielcintra10/django-accounts-api.git .
```
### Virtual environment
Create a virtual environment to run the project.
1) Inside the root directory open a terminal and use the following command 
to create a virtual environment.

```
python -m venv venv
```
2) Now activate the virtual environment with the following command.
#### windows machine
```
venv\Scripts\activate.bat
```

#### mac/linux
```
source venv/bin/activate
```

You will know your virtual environment is active when your terminal displays the following:
```
(venv) path\to\project\
```

### Project Requirements 
Let's go ahead and install the project requirements. 
Add the following code to you terminal.
```
pip install -r requirements.txt
```

### Secrets and Environment Variables
It is good practice to separate sensitive information from your project. 
I have installed a package called 'python-dotenv' that helps me manage secrets easily. 
Let's go ahead and create an .env file to store information that is specific to our working environment. 
Use the following command in your terminal.

#### windows machine
```
copy .env.example .env
```
#### mac/linux
```
cp .env.example .env
```
You can use the .env file to store API keys, secret_keys, app_passwords, db_secret_info,
and you will gain access to these in the Django app.
Use the .env.example file as a reference to configure the environment variables that are required in this project.

### Database migrations
Before starting the project, it is necessary to create a database. The project is structured to use Postgres SQL 
databases. If you need to use another database management system, you need to make extra configurations in the settings.py 
file to make the project work correctly.  
Remember after creating the database, create the necessary environment variables to achieve the correct connection 
between the database and Django.
Then let's create the database tables.
Use the following command:

~~~~
python manage.py migrate
~~~~

### Administration Site
You need a user with administrator permissions specially to access to the admin site,
you can run the following command and follow the instructions to create a superuser

~~~~
python manage.py createsuperuser
~~~~

### Test
To guarantee the quality of the project several tests were carried out, to execute these tests 
you simply have to execute the following command:

~~~
python manage.py test
~~~

### Run the project
Now you can run the server:

~~~
python manage.py runserver
~~~



***
***

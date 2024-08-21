# Team *Galin* Major Group project

# SETTINGS.PY IS OMITTED TO KEEP SECRET KEY PRIVATE

## Team members
The members of the team are:
- *REUBEN ATENDIDO*
- *RICKY BROWN*
- *YUSHENG LU*
- *OLIVER MACPHERSON*
- *GALIN MIHAYLOV*
- *MAKSIM VEPREV*

## Project structure
The project is called `personal_spending_tracker`.  It currently consists of a single app `tracker` where all functionality resides.

## Deployed version of the application
The deployed version of the application can be found at *http://rbn4atd.pythonanywhere.com/*.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.

## Superuser
Email: admin@email.com
Password: Password123

## User
Email: james@kcl.ac.uk
Password: Password123

More details can be found within the seeder file.


## Sources
The packages used by this application are specified in `requirements.txt`

Partial implementation of open source tutorial on YouTube. https://www.youtube.com/watch?v=YXmsi13cMhw&t=2075s&ab_channel=SelmiTech



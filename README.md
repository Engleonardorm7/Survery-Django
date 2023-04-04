# Django Project - Polls

This is a simple Django project that demonstrates the use of views and urls.

## Installation
To run this project, you need to have Python 3 and Django installed on your system.

## Clone the repository:
sh

``` $ git clone https://github.com/Engleonardorm7/Survery-Django
$ cd polls```

## Install the dependencies:

``` $ pip install -r requirements.txt
Run the migrations:```

``` $ python manage.py migrate```

##Create a superuser:

``` $ python manage.py createsuperuser```

## Run the development server:

``` $ python manage.py runserver ```

##Usage
You can access the polls app at http://localhost:8000/polls/.

##The available views are:

Index: displays a list of all the available questions in the database.
Detail: displays the details of a specific question.
Results: displays the results of a specific question.
Vote: allows the user to vote on a specific question.
The available URLs are:

/polls/
/polls/holi/
/polls/int:pk/
/polls/int:pk/results/
/polls/int:question_id/vote/
/polls/login/
##Views
##IndexView
Displays a list of all the available questions in the database.

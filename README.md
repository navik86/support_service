# The "Support_service" application


## About the app
The application is a REST API that allows you to register users. The user can create and send tickets.
The support sees all tickets and can respond to them. Support can change ticket statuses.
The user can view the support response and add a new message.

I used Django with the Django REST framework.



## How to use

* Main view is under: http://127.0.0.1:8000/api
Here you can view users and tickets.

* By this URL http://127.0.0.1:8000/api/users you can view the list of users

* By this URL http://127.0.0.1:8000/api/tickets you can view the list of tickets.
To view the detailed etiquette, click on the link in the list of tickets.

* By this URL http://127.0.0.1:8000/api/tickets /"№ ticket" /messages/ you can view the list of tickets.
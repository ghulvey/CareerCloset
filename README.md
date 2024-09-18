# GoldenOpportunities

## Problem Statement

Today students need help finding professional clothing as they prepare to enter the workforce. Kent State Career Services offers the Career Closet which provides free professional clothing to any Kent State student. The Career Closet is anonymous for students to visit the closet in person and mark down what they take. Currently, the closet can only be viewed in person at career services, which can limit access for students as they may not know what's in stock before coming or may not be able to have the time to check in depth what the closet has. One of the main pain points for the current system is for regional campus students, students would like to know what is available before making a possible hour's drive. We aim to create a platform for Kent State students to browse the closet 24/7 digitally similar to a shopping site like Amazon. Students can reserve clothing and pick it up in person using an anonymous ID. Other features could include scheduling a day and time for donations and pickups and submitting an application to the professional clothing fund, which provides grants to purchase new clothes. Career Service staff will have a backend interface to submit images of clothing and process incoming requests. The customer for this system is Kent State Career Services, the users would consist of all Kent State students, student employees, and office staff. The stakeholder for this project is the executive director of career services, Justin Edwards. Users of this application will not need to have a computer science background, no user should have to interact directly with the database, all interaction should be done through a web application. Some potential risks are if someone does not get an item through the website and this is not reflected in the database; another could be a person's allergy to certain clothing items. We can assume that there is proper infrastructure to support this project; and, all workers will have knowledge of this updated system. We can also assume all the clothing in the system is in good condition to be worn.The system would be composed of a front-end web application, and a backend API and database.

## Technologies

- Django

## Installation

pip install django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

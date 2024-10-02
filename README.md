# GoldenOpportunities

## Problem Statement

Today students need help finding professional clothing as they prepare to enter the workforce. Kent State Career Services offers the Career Closet which provides free professional clothing to any Kent State student. The Career Closet is anonymous for students to visit the closet in person and mark down what they take. Currently, the closet can only be viewed in person at career services, which can limit access for students as they may not know what's in stock before coming or may not be able to have the time to check in depth what the closet has. One of the main pain points for the current system is for regional campus students, students would like to know what is available before making a possible hour's drive. We aim to create a platform for Kent State students to browse the closet 24/7 digitally similar to a shopping site like Amazon. Students can reserve clothing and pick it up in person using an anonymous ID. Other features could include scheduling a day and time for donations and pickups and submitting an application to the professional clothing fund, which provides grants to purchase new clothes. Career Service staff will have a backend interface to submit images of clothing and process incoming requests. The customer for this system is Kent State Career Services, the users would consist of all Kent State students, student employees, and office staff. The stakeholder for this project is the executive director of career services, Justin Edwards. Users of this application will not need to have a computer science background, no user should have to interact directly with the database, all interaction should be done through a web application. Some potential risks are if someone does not get an item through the website and this is not reflected in the database; another could be a person's allergy to certain clothing items. We can assume that there is proper infrastructure to support this project; and, all workers will have knowledge of this updated system. We can also assume all the clothing in the system is in good condition to be worn.The system would be composed of a front-end web application, and a backend API and database.

## Technologies

- Django
- Bootstrap

## Installation

```bash
# Install Dependencies
pip install -r requirements.txt

# Migrate the database
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations access
python manage.py migrate access

# Create a admin user
python manage.py createsuperuser

# Create groups and map permission
python manage.py create_groups

# Run the server
python manage.py runserver

#Populate DB with sample clothes
python manage.py loaddata exampledata.json
```

### Microsoft Entra Setup

Copy the secrets from the `SECRET` file in Google Drive and paste them in the `secrets.py` file. We should find a better way to store these secrets in the future.

```python
ENTRA_CLIENT_ID = 'SECRET'
ENTRA_CLIENT_SECRET = 'SECRET'
```

Click login with Flashline and log in with your Kent State credentials.

**(Optional)** Grant admin permissions to your Flashline account.

- Go to `/admin`
- Login with the superuser account
- Go to `Users` and click on your user, the one with a random-looking username
- Check the `is_staff` and `is_superuser` boxes
- Save
- Logout and log in with your Flashline account
- Personal information (first name, last name) will now be mapped to your user account

### Custom Bootstrap Theme

To customize the Bootstrap theme edit the custom.scss file in `/kent-boostrap/scss/custom.scss` and run the following command to compile the scss file.

```bash
cd kent-bootstrap
npm install
npm run build-css
```

The compiled css file will be placed in `/static/kent-bootsrap.css`

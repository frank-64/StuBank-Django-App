# StuBank - Online Banking Website  

Newcastle University 2020/21 Software Engineering Team Project

## Local Installation and execution
<strong>We recommend using the website rather than installing the project locally</strong>

Clone the project to your machine.

Create a virtual environment using python virtualenv in the root directory.

Install all packages outlined in the requirements.txt file like so
```commandline
pip install -r requirements.txt
```

To run the web application locally, navigate to the project directory within the pycharm terminal and type:
```commandline
py manage.py runserver
```
Click the link provided in the terminal

## Usage
This website can be found here [stubank.tk](https://stubank.tk)

## About the systems involved
The website is hosted using Amazon Web Service with all of the service available under their 12 month free trial.

### Backend
* We are using EC2 which is Amazon's Elastic Compute Cloud.
    - We created an Ubuntu server instance which hosts the website.
    - This instance has an Nginx and Gunicorn installed working together.
    - Nginx is a web server and reverse proxy meaning it redirects any of the requests from the Django instances 
    to Gunicorn to for it to handle. Nginx also serves any static files too such as CSS, images and files.
### Database
* We use Amazon's Relational Database Service (RDS) to contain our database.
* Our Django application is connected to this database and performs CRUD operations on either localhost or the hosted
website.

## Testing
We have created a series of unit tests which can be run to check the functionality of the different pages 
of the web application. To run these, type into the command line:

```commandline
py manage.py test
```

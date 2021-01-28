# StuBank - Online Banking Website  

Newcastle University 2020/21 Software Engineering Team Project

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





 

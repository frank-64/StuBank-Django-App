# StuBank - Online Banking Website  

Newcastle University 2020/21 Software Engineering Team Project

## Local Installation
<strong>We recommend using the website rather than installing the project locally</strong>
Clone the project to your machine.

Install all packages outlined in the requirements.txt file like so
```commandline
pip install -r requirements.txt
```


## Local execution
<strong>We recommend using the website rather than installing the project</strong>
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

## Example Customer Account
We have created a pre-populated customer account specifically for marking purposes containing a 
set of transactions, payees and money pots. This will allow you to view the full potential of
the web application, without you needing to spend the time creating this data yourself.

Navigate to the login page and enter the details below. Scan the QR code with the Google 
Authenticator app to retrieve a six digit code for the Otp token section.

Username: <b>bigstu22</b> 
Password: <b>xVy2Lbzj?</b> 

<p align="center">
<img src="media/qr_codes/bigstu22.png" width="200" height="200">
</p>

Follow this link to retrieve the QR code if the above image isn't loading:
https://imgur.com/3Nea4CU

For security purposes, the CVC number and card expiry date isn't displayed on the account. 

The accounts CVC number is: <b>434</b> and expiry date is: <b>19/01/2026</b>

These will be of particular use going through the process of adding a new payee.

## Example Helper Account
We have also created a helper account as this must be done manually through the built in Django admin interface, this is
how we intended to make the accounts as users should not be able to make themselves a helper.

Helpers login in to the same place as customers and also use 2-Factor-Authentication.

Navigate to the login page and enter the details below. Scan the QR code with the Google 
Authenticator app to retrieve a six digit code for the Otp token section.

Username: <b>Helper-Joel</b> 
Password: <b>zzQu1d9!</b> 

<p align="center">
<img src="media/qr_codes/Helper-Joel.png" width="200" height="200">
</p>

Follow this link to retrieve the QR code if the above image isn't loading:
https://imgur.com/a/JNVszye

## Testing
We have created a series of unit tests which can be run to check the functionality of the different pages 
of the web application. To run these, type into the command line:

```commandline
py manage.py test
```



 

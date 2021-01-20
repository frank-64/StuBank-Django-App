# StuBank - Online Banking Website  

Newcastle University 2020/21 Software Engineering Team Project

## Installation
Install all packages outlined in the requirements.txt file

## Usage
To run the web application locally, navigate to the project directory within the pycharm terminal and type:
```commandline
py manage.py runserver
```
Click the link provided in the terminal

Alternatively, you can access the online version here at [https://stubank.tk](stubank.tk)

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
## Testing
We have created a series of unit tests which can be run to check the functionality of the different pages 
of the web application. To run these, type into the command line:

```commandline
py manage.py test
```



 

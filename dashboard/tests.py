from django.http import request
from django.test import TestCase, RequestFactory
from .models import *
from .views import *

def setUpUser():
    user = User.objects.create(username='test_customer', email='customer@test.com', first_name='Bobby',
                               last_name='Hummer', is_customer=1)
    user.set_password('password')
    user.save()
    return user

class CheckPayeeTestCase(TestCase):
    # Create the customer and helper objects in the database for testing
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username='test_customer', email='customer@test.com', first_name='Bobby',
                                            last_name='Hummer', is_customer=1)
        self.user.set_password('password')

        self.user_payee = User.objects.create(username='test_payee', email='helper@test.com', first_name='Pegasus',
                                          last_name='Smores', is_customer=0, is_helper=1)
        self.user_payee.set_password('qwerty')

        self.payee = Customer.objects.create(user=self.user_payee, account_num=2222222, sort_code='42-04-20',
                                                 balance=100.00, available_balance=100.00)
        self.user.save()
        self.payee.save()

    def test_payee_creation(self):
        self.assertEqual(self.user.username, 'test_customer')
        self.assertEqual(self.payee.user.username, 'test_payee')

    def test_check_payee_exists(self):
        payee_object = Customer.objects.filter(sort_code=self.payee.sort_code,
                                                 account_num=self.payee.account_num,
                                                 user__first_name=self.payee.user.first_name,
                                                 user__last_name=self.payee.user.last_name)

        self.assertEqual(True, payee_object.exists())

    def test_payee_same_as_user(self):
        payee_object = Customer.objects.filter(sort_code=self.payee.sort_code,
                                                 account_num=self.payee.account_num,
                                                 user__first_name=self.payee.user.first_name,
                                                 user__last_name=self.payee.user.last_name)

        self.assertEqual(True, payee_object[0].user == self.payee.user)

class AddPayeeTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username='test_customer', email='customer@test.com', first_name='Bobby',
                                            last_name='Hummer', is_customer=1)
        self.user.set_password('password')

        self.user_payee = User.objects.create(username='test_payee', email='helper@test.com', first_name='Pegasus',
                                          last_name='Smores', is_customer=0, is_helper=1)
        self.user_payee.set_password('qwerty')

        self.payee = Customer.objects.create(user=self.user_payee, account_num=2222222, sort_code='42-04-20',
                                                 balance=100.00, available_balance=100.00)
        self.user.save()
        self.payee.save()




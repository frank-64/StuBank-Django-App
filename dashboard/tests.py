import json
from http import HTTPStatus

from django.contrib.auth import authenticate
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import *

from urllib.parse import urlencode

from django.http import request
from django.test import TestCase, RequestFactory
from .models import *
from .views import *
from dashboard import forms


def setUpUser(username):
    user = User.objects.create(username=username, email='customer@test.com', first_name='Bobby',
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
        self.client.login(username='test_customer', password='password')

    def test_add_valid_payee(self):
        request = self.request_factory.get(reverse('addpayee'))
        request.user = self.user


class MoneyPotCreateViewTestCase(TestCase):

    # Set up user and customer objects and log in
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

    # Test get request for create view
    def test_get(self):
        response = self.client.get(reverse('add_money_pot'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test money pot is created when post request sent
    def test_post_success(self):
        response = self.client.post(reverse('add_money_pot'), data={'name': 'test_pot', 'target_balance': 1000})
        pot = MoneyPot.objects.get(name='test_pot')

        self.assertRedirects(response, reverse('money_pots'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(pot is not None)

    # Test money pot is not created when incorrect data is input
    def test_post_fail(self):
        response = self.client.post(reverse('add_money_pot'), data={'name': 'test_pot'})
        pot_exists = MoneyPot.objects.filter(name='test_pot').exists()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(pot_exists)


class MoneyPotDepositViewTestCase(TestCase):

    # Set up and login customer, create a test money pot
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

        self.pot = MoneyPot.objects.create(customer=self.customer, name='test_deposit_pot', target_balance=500)
        self.pot.save()
        self.pk = self.pot.pk

    # Test get request for deposit view
    def test_get(self):
        response = self.client.get(reverse('deposit_money_pot', kwargs={'pk': self.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test money is correctly deposited into pot when post request sent, and check if user available balance has updated
    def test_post_success(self):
        response = self.client.post(reverse('deposit_money_pot', kwargs={'pk': self.pk}), data={'amount': 50})
        pot = MoneyPot.objects.get(pk=self.pk)
        customer = Customer.objects.get(pk=self.customer.pk)

        self.assertRedirects(response, reverse('money_pots'))
        self.assertEqual(pot.pot_balance, 50)
        self.assertEqual(customer.available_balance, 50)

    # Test no money is deposited when incorrect form data is input
    def test_post_fail(self):
        response = self.client.post(reverse('deposit_money_pot', kwargs={'pk': self.pk}), data={'amount': '#########'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.failIf(response.context['form'].is_valid())


class MoneyPotDeleteViewTestCase(TestCase):

    # Set up and login customer, create a test money pot
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

        self.pot = MoneyPot.objects.create(customer=self.customer, name='test_delete_pot', target_balance=500)
        self.pot.save()
        self.pk = self.pot.pk

    # Test get request for delete view
    def test_get(self):
        response = self.client.get(reverse('delete_money_pot', kwargs={'pk': self.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test if money pot is deleted when delete button pressed
    def test_post_success(self):
        response = self.client.post(reverse('delete_money_pot', kwargs={'pk': self.pk}))
        pot_exists = MoneyPot.objects.filter(pk=self.pk).exists()

        self.assertRedirects(response, reverse('money_pots'))
        self.assertFalse(pot_exists)


class MoneyPotUpdateViewTestCase(TestCase):

    # Set up and login customer, create a test money pot
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

        self.pot = MoneyPot.objects.create(customer=self.customer, name='test_update_pot', target_balance=500)
        self.pot.save()
        self.pk = self.pot.pk

    # Test get request for update view
    def test_get(self):
        response = self.client.get(reverse('update_money_pot', kwargs={'pk': self.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test pot details are updated after post request sent
    def test_post_success(self):
        response = self.client.post(reverse('update_money_pot', kwargs={'pk': self.pk}), data={'name': 'updated_name',
                                                                                               'target_balance': 1000})
        pot = MoneyPot.objects.get(pk=self.pk)

        self.assertRedirects(response, reverse('money_pots'))
        self.assertEqual(pot.name, 'updated_name')
        self.assertEqual(pot.target_balance, 1000)

    # Test pot details are not updated if invalid data is input in form
    def test_post_fail(self):
        response = self.client.post(reverse('update_money_pot', kwargs={'pk': self.pk}), data={'name': 'updated_name',
                                                                                               'target_balance': '#########'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.failIf(response.context['form'].is_valid())


class PDFDownloadTestCase(TestCase):

    # Set up user and customer objects and log in
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

    # Test if correct file type and name is downloaded when get request sent for statement view
    def test_pdf_download(self):
        response = self.client.get(reverse('statement'))

        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename=' + self.user.username +
                          '_statement.pdf')


# TODO: Test post fail and success for all tests below

class PayeeTransferViewTestCase(TestCase):

    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

        self.user_2 = setUpUser('test_customer2')
        self.customer_2 = Customer.objects.create(user=self.user_2)

        self.payee = Payee(PayeeID=self.customer_2, User=self.user)
        self.payee.save()

    # Test get request for payee transfer view
    def test_get(self):
        response = self.client.get(reverse('transfer'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_success(self):
        response = self.client.post(reverse('transfer'), data={'Payee': self.payee.pk, 'Amount': 15,
                                                               'Comment': 'Test transfer', 'Category': 'Dining Out'})
        customer = Customer.objects.get(pk=self.customer.pk)
        customer_2 = Customer.objects.get(pk=self.customer_2.pk)

        self.assertRedirects(response, reverse('dashboard_home'))
        self.assertEqual(customer_2.balance, 115)
        self.assertEqual(customer.balance, 85)


class PayeeDetailViewTestCase(TestCase):

    # Set up user and customer objects and log in
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

    # Test get request for payee detail view
    def test_get(self):
        response = self.client.get(reverse('viewpayee'))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class AddPayeeViewTestCase(TestCase):

    # Set up user and customer objects and log in
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

        self.user_2 = setUpUser('test_customer2')
        self.customer_2 = Customer.objects.create(user=self.user_2)
        self.customer_2.account_num = 123456789
        self.customer_2.sort_code = '12-34-56'
        self.customer_2.save()

    # Test get request for add payee view
    def test_get(self):
        response = self.client.get(reverse('addpayee'))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ExpenditureOverviewViewTestCase(TestCase):

    # Set up user and customer objects and log in
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

    # Test get request for expenditure overview
    def test_get(self):
        response = self.client.get(reverse('overview'))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class HelpPageViewTestCase(TestCase):

    # Set up user and customer objects and log in
    def setUp(self):
        self.user = setUpUser('test_customer')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

    # Test get request for help page
    def test_get(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class LiveChatTestCase(TestCase):
    pass


'''class LiveChatTestCase(TestCase):

    # Set up user and customer objects and log in
    def setUp(self):
        self.user = setUpUser()
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

    # Test get request for live chat page
    def test_get(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, HTTPStatus.OK)'''

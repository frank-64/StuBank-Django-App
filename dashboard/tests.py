from http import HTTPStatus

from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse

from .models import *


# Create your tests here.

def setUpUser():
    user = User.objects.create(username='test_customer', email='customer@test.com', first_name='Bobby',
                               last_name='Hummer', is_customer=1)
    user.set_password('password')
    user.save()
    return user


class AddMoneyPotViewTestCase(TestCase):

    def setUp(self):
        self.user = setUpUser()
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

    def test_get(self):
        response = self.client.get(reverse('add_money_pot'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_success(self):
        response = self.client.post(reverse('add_money_pot'), data={'name': 'test_pot', 'target_balance': 1000})
        pot = MoneyPot.objects.get(name='test_pot')

        self.assertRedirects(response, reverse('money_pots'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(pot is not None)

    def test_post_fail(self):
        response = self.client.post(reverse('add_money_pot'), data={'name': 'test_pot'})
        pot_exists = MoneyPot.objects.filter(name='test_pot').exists()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(pot_exists)


class DepositMoneyPotView(TestCase):

    def setUp(self):
        self.user = setUpUser()
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='test_customer', password='password')

        self.pot = MoneyPot.objects.create(customer=self.customer, name='test_deposit_pot', target_balance=500)
        self.pot.save()
        self.pk = self.pot.pk

    def test_get(self):
        response = self.client.get(reverse('deposit_money_pot', kwargs={'pk': self.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_success(self):
        response = self.client.post(reverse('deposit_money_pot', kwargs={'pk': self.pk}), data={'amount': 100})
        pot = MoneyPot.objects.get(pk=self.pk)

        self.assertRedirects(response, reverse('money_pots'))
        self.assertEqual(pot.pot_balance, 100)

    def test_post_fail(self):
        response = self.client.post(reverse('deposit_money_pot', kwargs={'pk': self.pk}), data={'amount': '#########'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.failIf(response.context['form'].is_valid())

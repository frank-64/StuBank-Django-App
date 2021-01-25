from http import HTTPStatus
from django.test import TestCase, RequestFactory, Client
from .views import *


def setUpUser(username):
    """
        Written by: Ed
        Purpose: Set up a default user for use during testing
    """

    user = User.objects.create(username=username, email='customer@test.com', first_name='Bobby',
                               last_name='Hummer', is_customer=1)
    user.set_password('password')
    user.save()
    return user


class CheckPayeeTestCase(TestCase):
    """
        Written by: Frankie
        Purpose: To test if the checking of payee functionality works as intended and a payee is successfully verified
    """

    # Create the customer and helper objects in the database for testing
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username='test_customer', email='customer@test.com', first_name='Bobby',
                                        last_name='Hummer', is_customer=1)
        self.user.set_password('password')

        self.user_payee = User.objects.create(username='test_payee', email='helper@test.com', first_name='Pegasus',
                                              last_name='Smores', is_customer=1)
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


class MoneyPotCreateViewTestCase(TestCase):
    """
        Written by: Ed
        Purpose: To test if the MoneyPotCreateView successfully creates a new money pot in the database when valid
                information is input.
    """

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
    """
        Written by: Ed
        Purpose: To test if the MoneyPotDepositView successfully deposits money into the correct money pot when valid
                information is input.
    """

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
    """
        Written by: Ed
        Purpose: To test if the MoneyPotDeleteView successfully deletes the correct money pot
    """

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
    """
        Written by: Ed
        Purpose: To test if the MoneyPotUpdateView successfully updates the correct money pot with a new target value
    """

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
    """
        Written by: Ed
        Purpose: To test that the pdf_view function successfully generates a PDF file when requested
    """

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
    """
        Written by: Ed
        Purpose: To test that the PayeeTransferView successfully transfers money to the correct payee
    """

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

    '''
    def test_post_success(self):
        response = self.client.post(reverse('transfer'), data={'Payee': self.payee.pk, 'Amount': 15,
                                                               'Comment': 'Test transfer', 'Category': 'Dining Out'})
        customer = Customer.objects.get(pk=self.customer.pk)
        customer_2 = Customer.objects.get(pk=self.customer_2.pk)

        self.assertRedirects(response, reverse('dashboard_home'))
        self.assertEqual(customer_2.balance, 115)
        self.assertEqual(customer.balance, 85)'''


class PayeeDetailViewTestCase(TestCase):
    """
        Written by: Ed
        Purpose: To test that a PayeeDetailView get request is successful
    """

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
    """
        Written by: Ed
        Purpose: To test that a AddPayeeView get request is successful
    """

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
    """
        Written by: Ed
        Purpose: To test that a ExpenditureOverviewView get request is successful
    """

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
    """
        Written by: Ed
        Purpose: To test that a HelpPageView get request is successful
    """

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

    # Set up user and customer objects and log in
    def setUp(self):
        self.user = setUpUser('BobbyBoy')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='BobbyBoy', password='password')


        self.helper = User.objects.create(username='Helper-Jacob', email='helper-jacob@test.com', first_name='Jacob',
                                              last_name='Steed', is_helper=1)
        self.helper.set_password('password')
        self.helper = Helper.objects.create(user=self.helper)

    # Test get request for live chat page
    def test_get(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Checking that customer and helper are correct role
    def test_role(self):
        self.assertEqual(self.customer.user.is_customer, True)
        self.assertEqual(self.helper.user.is_helper, True)

    def test_livechat_get(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_freeze_account_before_perms(self):
        self.client.login(username='Helper-Jacob', password='password')
        response = self.client.get(reverse('freeze_card', kwargs={'pk': self.user.pk}))
        print(response)
        self.assertEqual(self.user.is_active, False)

from django.test import TestCase
from .models import *
from .views import *


# If your tests rely on database access such as creating or querying models, be sure to create your test classes as
# subclasses of django.test.TestCase rather than unittest.TestCase.

def setUpUser():
    """
        Written by: Ed
        Purpose: Setup and return a user for use during testing
    """

    user = User.objects.create(username='test_customer', email='customer@test.com', first_name='Bobby',
                               last_name='Hummer', is_customer=1)
    user.set_password('password')
    user.save()
    return user


class SignUpTestCase(TestCase):
    """
        Written by: Ed
        Purpose: Test the sign up process successfully creates a user
    """

    # Create the customer and helper objects in the database for testing
    def setUp(self):
        user_customer = User.objects.create(username='test_customer', email='customer@test.com', first_name='Bobby',
                                            last_name='Hummer', is_customer=1)
        user_customer.set_password('password')

        user_helper = User.objects.create(username='test_helper', email='helper@test.com', first_name='Pegasus',
                                          last_name='Smores', is_customer=0, is_helper=1)
        user_helper.set_password('qwerty')

        user_customer.save()
        user_helper.save()

    # Test standard user accounts are created
    def test_user_creation(self):
        user = User.objects.get(username='test_customer')
        self.assertEqual(user.username, 'test_customer')

    # Test customer accounts are created with correct is_customer field values for their corresponding user
    def test_customer_creation(self):
        user = User.objects.get(username='test_customer')
        customer = Customer.objects.create(user=user)
        self.assertEqual(user.is_customer, 1)
        self.assertEqual(user.is_helper, 0)
        self.assertEqual(customer.user, user)

    # Test helper accounts are created with correct is_helper field values for their corresponding user
    def test_helper_creation(self):
        user = User.objects.get(username='test_helper')
        helper = Helper.objects.create(user=user)
        self.assertEqual(user.is_customer, 0)
        self.assertEqual(user.is_helper, 1)
        self.assertEqual(helper.user, user)


class SignInTestCase(TestCase):
    """
        Written by: Ed
        Purpose: Test the Sign in process successfully signs a user in
    """

    # Create the user object in the database for testing
    def setUp(self):
        user = setUpUser()

    # Test that login works when user details are correct
    def test_correct_details(self):
        user = authenticate(username='test_customer', password='password')
        self.assertTrue((user is not None) and user.is_authenticated)

    # Test that no users are returned and they are not authenticated when the incorrect username in used
    def test_wrong_username(self):
        user = authenticate(username='#########', password='password')
        self.assertFalse((user is not None) and user.is_authenticated)

    # Test that no users are returned and they are not authenticated when the incorrect password in used
    def test_wrong_password(self):
        user = authenticate(username='test_customer', password='#########')
        self.assertFalse((user is not None) and user.is_authenticated)


class RegisterViewTestCase(TestCase):
    """
        Written by: Ed
        Purpose: Test the register page successfully allows valid details and rejects invalid details
    """

    def setUp(self):
        pass

    # Test if user is redirected to totp page if they enter valid registration details
    def test_correct_details(self):
        response = self.client.post(reverse('register'), data={'username': 'test_customer', 'email': 'test@test.com',
                                                        'first_name': 'Test', 'last_name': 'User',
                                                        'password1': 'password', 'password2': 'password'})
        self.assertRedirects(response, reverse('totp_create'))

    # Test to check if user cannot submit form if they enter invalid registration details
    def test_wrong_details(self):
        response = self.client.post(reverse('register'), data={'username': 'test_customer', 'email': 'test@test.com',
                                                               'first_name': 'Test', 'last_name': 'User',
                                                               'password1': 'password', 'password2': '#########'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())

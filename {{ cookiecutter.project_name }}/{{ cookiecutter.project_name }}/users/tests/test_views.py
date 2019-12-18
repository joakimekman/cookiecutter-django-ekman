from django.test import TestCase, Client
from django.urls import reverse
from {{ cookiecutter.project_name }}.users.models import User


class CreateViewTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.client = Client()
    cls.user = User.objects.create_user(username="anon", email="anon@test.com")
    cls.url = reverse('user:register')

  def test_unauthorized_GET(self):
    """ Ensures a 200 is returned and that the right template is rendered
    when requesting to view the create page while unauthorized. """
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'registration/register.html')

  def test_authorized_GET(self):
    """ Ensures a 302 redirect to detail page is performed when requesting
    to view the create page while authorized. """
    self.client.force_login(self.user)
    response = self.client.get(self.url)
    self.assertRedirects(
      response, 
      reverse('user:detail', kwargs={"username": self.user}),
      status_code=302,
      target_status_code=200
    )

  def test_POST_and_success_url(self):
    """ Ensures that a user can be created and automatically logged in. """
    response = self.client.post(self.url, {
      'username': 'test',
      'first_name': 'anon',
      'last_name': 'nymous',
      'email': 'test@test.com',
      'password1': 'pw',
      'password2': 'pw',
    })
    self.assertTrue(User.objects.filter(username="test").exists())
    self.assertRedirects(
      response, 
      reverse('user:detail', kwargs={"username": "test"}),
      status_code=302,
      target_status_code=200
    )
  

class DetailViewTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.client = Client()
    cls.user = User.objects.create_user(username="anon", email="anon@test.com")
    cls.url = reverse('user:detail', kwargs={"username": cls.user})

  def test_GET_active_user(self):
    """ Ensures a 200 is returned and that the right template is rendered
    when requesting to view the detail page of an active user. """
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'users/detail.html')

  def test_GET_inactive_user(self):
    """ Ensures a 404 is raised when requesting to view the detail page
    of an inactive user. """
    inactive_user = User.objects.create_user(username="anon2", email="anon2@test.com", is_active=False)
    response = self.client.get(reverse('user:detail', kwargs={"username": inactive_user}))
    self.assertEqual(response.status_code, 404)  

  def test_GET_non_existent_user(self):
    """ Ensures a 404 is raised when requesting to view the detail page
    of a non existent user. """
    response = self.client.get(reverse('user:detail', kwargs={"username": "sdf"}))
    self.assertEqual(response.status_code, 404)

  def test_get_object(self):
    """ Ensure object is the user specified in the URL. """
    response = self.client.get(self.url)
    self.assertEqual(response.context['object'], self.user)


class LoginViewTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.client = Client()
    cls.user = User.objects.create_user(username="anon", email="anon@test.com")
    cls.url = reverse('user:login')

  def test_unauthorized_GET(self):
    """ Ensures a 200 is returned and that the right template is rendered
    when requesting to view the login page while unauthorized. """
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'registration/login.html')

  def test_authorized_GET(self):
    """ Ensures a 302 redirect to detail page is performed when requesting
    to view the login page while authorized. """
    self.client.force_login(self.user)
    response = self.client.get(self.url)
    self.assertRedirects(
      response, 
      reverse('user:detail', kwargs={"username": self.user}),
      status_code=302,
      target_status_code=200
    )


class RedirectViewTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.client = Client()
    cls.user = User.objects.create_user(username="anon", email="anon@test.com")
    cls.url = reverse('user:redirect')

  def test_authorized_GET(self):
    """ Ensures a 302 redirect to detail page is performed if authorized. """
    self.client.force_login(self.user)
    response = self.client.get(self.url)
    self.assertRedirects(
      response, 
      reverse('user:detail', kwargs={"username": self.user}),
      status_code=302,
      target_status_code=200
    )

  def test_unauthorized_GET(self):
    """ Ensures a 302 redirect to login page is performed if unauthorized. """
    response = self.client.get(self.url)
    self.assertRedirects(
      response, 
      '/login/?next=/~redirect/', 
      status_code=302, 
      target_status_code=200
    )


class UpdateViewTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.client = Client()
    cls.user = User.objects.create_user(username="anon", email="anon@test.com")
    cls.url = reverse('user:update_account', kwargs={"username": cls.user})

  def test_login_required(self):
    """ Ensures a 302 redirect to the login page is performed if unauthorized user try
    to access the update page. """
    response = self.client.get(self.url, follow=True)
    self.assertRedirects(
      response, 
      '/login/?next=/anon/update-account/',
      status_code=302,
      target_status_code=200
    )

  def test_GET_with_permission(self):
    """ Ensures a 200 is returned and that the right template is rendered
    if an authorized user with permission request to view the update page. """
    self.client.force_login(self.user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'users/update.html')

  def test_GET_without_permission(self):
    """ Ensures a 403 is raised if an authorized user without permission
    request to view the update page. 403 will also be raised if user does
    not exists. """
    user = User.objects.create_user(username="anon2", email="anon2@test.com")
    self.client.force_login(user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 403)

  def test_get_object(self):
    """ Ensures object is the user specified in the URL. """
    self.client.force_login(self.user)
    response = self.client.get(self.url)
    self.assertEqual(response.context['object'], self.user)

  def test_POST(self):
    """ Ensures a 302 redirect to the detail page is performed if user is
    successfully updated with valid POST data. """
    self.client.force_login(self.user)
    response = self.client.post(self.url, {
      "first_name": "test",
      "last_name": "nymous",
      "email": "anon@test.com",
    })
    self.user.refresh_from_db()
    self.assertRedirects(
      response, 
      reverse('user:detail', kwargs={"username": self.user}),
      status_code=302,
      target_status_code=200
    )
    self.assertEqual(self.user.first_name, 'test')


class DeleteViewTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.client = Client()
    cls.user = User.objects.create_user(username="anon", email="anon@test.com")
    cls.url = reverse('user:delete_account', kwargs={"username": cls.user})

  def test_login_required(self):
    """ Ensures a 302 redirect to the login page is performed if unauthorized user try
    to delete a user. """
    response = self.client.get(self.url)
    self.assertRedirects(
      response,
      '/login/?next=/anon/delete-account/',
      status_code=302,
      target_status_code=200
    )
  
  def test_GET_with_permission(self):
    """ Ensures a 302 redirect to index page is performed if an authorized user
    with permission succssfully "delete" the user account. """
    self.client.force_login(self.user)
    response = self.client.get(self.url)
    self.assertRedirects(
      response,
      reverse('index'),
      status_code=302,
      target_status_code=200
    )
    self.user.refresh_from_db()
    self.assertFalse(self.user.is_active)

  def test_GET_without_permission(self):
    """ Ensures a 403 is raised if an authorized user without permission
    request to delete the "delete" the user account. 403 will also be raised if 
     user does not exists. """
    user = User.objects.create_user(username="anon2", email="anon2@test.com")
    self.client.force_login(user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 403)


class PasswordChangeViewTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.client = Client()
    cls.user = User.objects.create_user(username="anon", email="anon@test.com", password="pw")
    cls.url = reverse('user:password_change', kwargs={"username": cls.user})

  def test_login_required(self):
    """ Ensures a 302 redirect to the login page is performed if unauthorized user try
    to access the password change page. """
    response = self.client.get(self.url)
    self.assertRedirects(
      response,
      '/login/?next=/anon/change-password/',
      status_code=302,
      target_status_code=200
    )

  def test_GET_with_permission(self):
    """ Ensures a 200 is returned and that the right template is rendered
    if an authorized user with permission request to view the password change page. """
    self.client.force_login(self.user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)

  def test_GET_without_permission(self):
    """ Ensures a 403 is raised if an authorized user without permission
    request to view the password change page. 403 will also be raised if user does
    not exists. """
    user = User.objects.create_user(username="anon2", email="anon2@test.com")
    self.client.force_login(user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 403)

  def test_POST_and_success_url(self):
    """ Ensures a 302 redirect to the detail page is performed if password is
    successfully updated with valid POST data. """
    self.client.force_login(self.user)
    data = {
      'old_password': 'pw',
      'new_password1': 'newpw',
      'new_password2': 'newpw',
    }
    response = self.client.post(reverse('user:password_change', kwargs={"username": self.user}), data)
    self.user.refresh_from_db()
    self.assertTrue(self.user.check_password('newpw'))
    self.assertRedirects(
      response,
      reverse('user:detail', kwargs={"username": self.user}),
      status_code=302,
      target_status_code=200
    )

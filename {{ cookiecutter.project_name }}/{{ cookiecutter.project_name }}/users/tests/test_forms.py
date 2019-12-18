from django.test import TestCase
from {{ cookiecutter.project_name }}.users.forms import CreateUserForm, UpdateUserForm
from {{ cookiecutter.project_name }}.users.models import User


class CreateUserFormTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.user = User.objects.create_user(username="anon", email="anon@test.com")

  def test_form_fields(self):
    """ Ensure the expected # of form fields are rendered. """
    form = CreateUserForm()
    self.assertEqual(len(form.fields), 6)

  def test_clean_username(self):
    """ Ensure a ValidationError is raised if username already exist. """
    form_data = {
      "username": "anon",
      "first_name": "anon",
      "last_name": "nymous",
      "email": "anon2@test.com",
      "password1": "pw",
      "password2": "pw"
    }
    form = CreateUserForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertEqual(form['username'].errors, ['Username has already been taken.'])

  def test_clean_email(self):
    """ Ensure a ValidationError is raised if email already exist. """
    form_data = {
      "username": "anon2",
      "first_name": "anon",
      "last_name": "nymous",
      "email": "anon@test.com",
      "password1": "pw",
      "password2": "pw"
    }
    form = CreateUserForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertEqual(form['email'].errors, ['Email has already been taken.'])


class UpdateUserFormTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.user = User.objects.create_user(username="anon", email="anon@test.com")
    cls.user2 = User.objects.create_user(username="anon2", email="anon2@test.com")

  def test_form_fields(self):
    """ Ensure the expected # of form fields are rendered. """
    form = UpdateUserForm()
    self.assertEqual(len(form.fields), 3)

  def test_clean_email(self):
    # providing same email (no changes)
    form = UpdateUserForm(instance=self.user, data={"email": "anon@test.com", "first_name": "anon", "last_name": "nymous"})
    self.assertTrue(form.is_valid())
    # providing email that already exist (user2.email)
    form = UpdateUserForm(instance=self.user, data={"email": "anon2@test.com", "first_name": "anon", "last_name": "nymous"})
    self.assertFalse(form.is_valid())
    self.assertEqual(form['email'].errors, ['Email has already been taken.'])
    # provide email that doesn't exist
    form = UpdateUserForm(instance=self.user, data={"email": "new@test.com", "first_name": "anon", "last_name": "nymous"})
    self.assertTrue(form.is_valid())





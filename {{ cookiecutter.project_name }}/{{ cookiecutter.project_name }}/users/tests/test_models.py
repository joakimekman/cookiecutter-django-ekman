from django.test import TestCase
from django.urls import reverse
from {{ cookiecutter.project_name }}.users.models import User

class UserModelTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.user = User.objects.create_user(username="anon")

  def test_get_absolute_url(self):
    expected_url = reverse("user:detail", kwargs={"username": self.user})
    self.assertTrue(self.user.get_absolute_url, expected_url)

  def test_str_representation(self):
    self.assertTrue(self.user, "anon")


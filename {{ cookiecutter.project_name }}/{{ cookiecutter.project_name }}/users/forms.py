from django import forms as django_forms
from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class CreateUserForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = forms.UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
        )

    def clean_username(self):
        username = self.cleaned_data["username"].lower()

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username has already been taken.")
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email has already been taken.")
        else:
            return email


class UpdateUserForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        initial_email = self.initial["email"]
        cleaned_email = self.cleaned_data["email"].lower()

        if initial_email == cleaned_email:
            return cleaned_email
        elif User.objects.filter(email=cleaned_email).exists():
            raise ValidationError("Email has already been taken.")
        else:
            return cleaned_email


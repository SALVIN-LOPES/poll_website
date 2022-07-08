from django import forms
from .models import User
from django.contrib.auth import authenticate, get_user_model, password_validation
import unicodedata
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "phone",
            'placeholder':'Phone Number'
        }

class EmailField(forms.CharField):

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "email",
            'placeholder':'Email'
        }

class NameField(forms.CharField):

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "name",
            'placeholder':'Name'
        }

class UserCreationForm(forms.ModelForm):

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'placeholder':'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'placeholder':'Password Confirmation'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("phone",'email','name')
        field_classes = {"phone": UsernameField,'email':EmailField,'name':NameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone','email','name']
        field_classes = {"phone": UsernameField}

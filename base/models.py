from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator

from .manager import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=True,
    )
    name = models.CharField(max_length=50, default="")
    phone_regex = RegexValidator(regex=r'^([0|+[0-9]{1,5})?([7-9][0-9]{9})$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[
        phone_regex], max_length=10, unique=True, null=True)  # validators should be a list
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)


class Poll(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length = 200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    def _str_(self):
        return str(self.id)

class ResponseModel(models.Model):
    response_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user",)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,related_name="poll",)
    choose = models.IntegerField()

    def _str_(self):
        return f'str(self.poll)+"==>"+str(self.choose)'



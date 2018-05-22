from datetime import date
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

from memberarea.apps.core.models import TimestampedModel


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):

    SEXES = (
        ('M', 'Male'),
        ('F', 'Female'),
        (' ', ''),
    )
    MEMBER_STATE = (
        ('A', 'Active'),
        ('P', 'Passive'),
    )

    # Personal information
    salutation = models.CharField(max_length=10, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    sex = models.CharField(max_length=1, choices=SEXES, default=' ')
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Club information
    member_id = models.IntegerField(db_index=True, unique=True)
    entry_date = models.DateField(blank=True, null=True)
    exit_date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=1, choices=MEMBER_STATE, default='A')

    # Security fields
    username = models.CharField(db_index=True, unique=True, max_length=201)
    pw_changed_at = models.DateField(default=date(1970, 1, 1))
    is_staff = models.BooleanField(default=False)
    token = None

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.last_name + ', ' + self.first_name

    def get_short_name(self):
        return self.first_name

    @property
    def display_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def pw_expires_at(self):
        return self.pw_changed_at + timedelta(days=settings.PASSWORD_EXPIRES_AFTER)

    @property
    def pw_is_expired(self):
        return self.pw_expires_at < date.today()

    @property
    def is_active(self):
        return (self.exit_date is None or self.exit_date > date.today()) and self.state == 'A'

    class Meta:
        ordering = ('last_name', 'first_name', )

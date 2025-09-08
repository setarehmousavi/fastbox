from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be entered!")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=35, blank=True)
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        # validators=[validators.RegexValidator(regex=r'^989[0-3,9]\d{8}$')],
        error_messages={'unique': _("The phone number already exists")},
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=35, unique=True)
    is_staff = models.BooleanField(default=False, help_text='To check whether a user is staff or not')
    is_active = models.BooleanField(default=True, help_text='To check whether user can login or not')
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    class Meta:
        verbose_name = _("MY User")
        verbose_name_plural = _("MY USERS")

    @property
    def get_full_name(self):
        """Returns the fullname of user"""
        return f"{self.first_name} {self.last_name}"

    def get_nickname(self):
        """return the nick name"""
        return self.first_name
    

class UserProfile(models.Model):
    GENDER_CHOICES = (
                    (0, "Male"),
                    (1, "Female")
    )
    ROLES = (
        (0, "USER"),
        (1, "admin"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(blank=True, null=True, upload_to='static/images/user')
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, default=0)
    role = models.PositiveIntegerField(choices=ROLES, default=0)

    def __str__(self):
        return f"{self.user.get_full_name}"
    
    def is_user(self):
        if self.role == 0:
            return True
        return False

    def is_admin(self):
        if self.role == 1:
            return True
        return False

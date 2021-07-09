from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    USER = 'USR', 'User'
    EMPLOYEE = 'EMPL', 'Employee'
    ADMIN = 'ADM', 'Admin'


class User(AbstractUser):

    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(
        'Логин',
        blank=False,
        unique=True,
        max_length=50,
        error_messages={
            'unique': "Пользователь с таким username уже существует.",
        },
    )
    role = models.CharField(
        default=Role.USER, choices=Role.choices, max_length=8)

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser
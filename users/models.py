from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint
from base.models import BaseModel 

ORDINARY_USER, ADMIN, MANAGER = ('ordinary_user', 'admin', 'manager')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
NEW, CONFIRM, DONE, DONE_PHOTO = ('new', 'confirm', 'done', 'done_photo')

class User(AbstractUser, BaseModel):  
    USER_TYPES = (
        (ORDINARY_USER, ORDINARY_USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER)
    )
    user_role = models.CharField(max_length=50, choices=USER_TYPES, default=ORDINARY_USER)
    user_status = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    auth_method = models.CharField(max_length=50, choices=[(VIA_EMAIL, 'Email'), (VIA_PHONE, 'Phone number')])
    auth_identifier = models.CharField(max_length=50, unique=True)

    photo = models.ImageField(upload_to='user_photos', default='default/user.jpg')
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender = models.CharField(max_length=1, choices=gender_choices)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class ConfirmUser(BaseModel): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    confirm_code = models.CharField(max_length=50, default=' '.join(str(randint(1, 100) % 10) for _ in range(4)))
    confirmed = models.BooleanField(default=False)
    user_type = models.CharField(max_length=50, choices=User.USER_TYPES, default=ORDINARY_USER)

    class Meta:
        db_table = 'confirm_users'

    def __str__(self):
        return self.user.username

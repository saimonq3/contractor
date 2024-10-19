import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from model_utils.choices import Choices
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .user_manager import UserAccountManager


def user_avatar__upload_to(instance, filename):
	"""
	Генерация пути загрузки аватарки пользователя
	"""
	return f"avatars/{get_random_string(16)}.{filename.split('.')[-1]}"


class User(AbstractUser):
	REQUIRED_FIELDS = ['phone_number', ]
	USERNAME_FIELD = 'email'

	SEX = Choices(
		('W', 'Женский'),
		('M', 'Мужской')
	)

	uuid = models.UUIDField(unique=True, null=True, default=uuid.uuid4, editable=False, verbose_name='UUID')
	email = models.EmailField(blank=False, unique=True, db_index=True, verbose_name=_('email'))
	email_verified = models.BooleanField(default=False, verbose_name='Email верифицирован')
	first_name = models.CharField(max_length=200, verbose_name='Имя')
	last_name = models.CharField(max_length=200, verbose_name='Фамилия')
	patronymic = models.CharField(max_length=200, default=None, blank=True, null=True, verbose_name='Отчество')
	phone_number = PhoneNumberField(null=True, blank=True, default=None, verbose_name='Телефон')
	country_code = models.CharField(max_length=2, blank=True, null=True, verbose_name='Код страны')
	sex = models.CharField(choices=SEX, max_length=1, blank=True, null=True, default=None, verbose_name='Пол')
	avatar = models.ImageField(
		default=None,
		blank=True,
		null=True,
		verbose_name='Аватарка',
		upload_to=user_avatar__upload_to
	)

	is_staff = models.BooleanField(default=False, verbose_name='Администратор')
	is_active = models.BooleanField(default=True, verbose_name='Активен')
	is_superuser = models.BooleanField(default=False, verbose_name='Супер-пользователь')

	objects = UserAccountManager()

	@property
	def fio(self) -> str:
		return ' '.join([w for w in [self.last_name, self.first_name, self.patronymic] if w])

	def get_short_name(self):
		return self.email

	def get_full_name(self):
		return self.email

	def __unicode__(self):
		return self.email

	def __str__(self):
		return f'{self.email} - {self.fio}'

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

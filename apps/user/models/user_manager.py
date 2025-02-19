from django.contrib.auth.base_user import BaseUserManager


class UserAccountManager(BaseUserManager):
	use_in_migrations = True

	def create_user(self, username, phone_number=None, password=None, **extra_fields):
		if not password:
			raise ValueError('Password must be provided')

		user = self.model(username=username, phone_number=phone_number, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password, phone_number=None, **extra_fields):
		user = self.model(phone_number=phone_number, username=username, is_staff=True, is_superuser=True, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
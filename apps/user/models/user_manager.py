from django.contrib.auth.base_user import BaseUserManager


class UserAccountManager(BaseUserManager):
	use_in_migrations = True

	def create_user(self, email, phone_number, password=None, **extra_fields):
		if not phone_number:
			raise ValueError('Phone must be provided')

		if not password:
			raise ValueError('Password must be provided')

		email = self.normalize_email(email)
		user = self.model(email=email, phone_number=phone_number, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, email, password, **extra_fields):
		user = self.model(phone_number=phone_number, email=email, is_staff=True, is_superuser=True, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
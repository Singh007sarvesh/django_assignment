from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class MyAccountManager(BaseUserManager):
	def create_user(self, email, first_name, last_name, phone,pincode, 
		password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not first_name:
			raise ValueError("Users must have an first name")
		if not last_name:
			raise ValueError("Users must have an last name")
		if not phone:
			raise ValueError("Users must have an phone")
		if not pincode:
			raise ValueError("Users must have an pincode")
		if not password:
			raise ValueError("Users must have an password")

		user  = self.model(
				email=self.normalize_email(email),
				first_name=first_name,
				last_name=last_name,
				phone=phone,
				pincode=pincode,
				password=password,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, last_name, phone, pincode, 
		password):
		user  = self.create_user(
				email=self.normalize_email(email),
				first_name=first_name,
				last_name=last_name,
				phone=phone,
				pincode=pincode,
				password=password,
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	# username 				= models.CharField(max_length=30, unique=True)
	# date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	# last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	first_name = models.CharField(max_length=50, null=False)
	last_name = models.CharField(max_length=50,null=False)
	address = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	state = models.CharField(max_length=50, null=True, blank=True)
	country = models.CharField(max_length=50, null=True, blank=True)
	pincode = models.IntegerField(null=False, blank=False)
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	password = models.CharField(max_length=300)
	

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name','phone','pincode','password']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True








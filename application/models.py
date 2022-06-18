from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff, 
            is_active=True,
            is_superuser=is_superuser, 
            last_login=now,
            date_joined=now, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
      return self._create_user(email, password, False, False, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
      user=self._create_user(email, password, True, True, **extra_fields)
      user.save(using=self._db)
      return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_tenant = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_pics')
    phone_number = models.CharField(max_length=10, unique=True, blank=True)

    def save_tenant(self):
        self.save()

    def __str__(self):
        return f"{self.user.username}"


class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Dr. {self.user.username}"

        

class Apartment(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='apartment_images', default='image.jpg')
    description = models.TextField(blank=True, null=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class ApartmentImages(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.ImageField("image")

    def __str__(self):
        return self.image.url


class RoomType(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.room_type


class RoomNumber(models.Model):
    room_type = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=255,)

    def __str__(self):
        return self.room_number


class Booking(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    room_number = models.OneToOneField(RoomNumber, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    stay_approved = models.BooleanField(verbose_name=("approved"),null=True, default=False)

    def __str__(self):
        if self.apartment:
            obj = self.apartment
        else:
            obj = self.room_number
            
        return f'{obj} {self.price}'


class Amenity(models.Model):
    description = models.TextField()
    apartment = models.ManyToManyField(Apartment, related_name='apartment_amenity')

    def __str__(self):
        return self.description


class HouseRule(models.Model):
    description = models.TextField()
    apartment = models.ManyToManyField(Apartment, related_name='apartment_rules')

    def __str__(self):
        return self.description


class Reviews(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    def __str__(self):
        return f'REview by {self.sender}'

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)
    country_image = models.ImageField(upload_to='country_image/', null=True, blank=True)

    def __str__(self):
        return self.country_name


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(80)], null=True, blank=True)
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,null=True,blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    ROLE_CHOICES = (
        ('client', 'client'),
        ('owner', 'owner')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'

class City(models.Model):
    city_name = models.CharField(max_length=30, unique=True)
    city_image = models.ImageField(upload_to='city_image/')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name

class Service(models.Model):
    service_name = models.CharField(max_length=32)
    service_image = models.ImageField(upload_to='service_image/')

    def __str__(self):
        return self.service_name


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=64)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_hotels')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hotel_stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    street = models.CharField(max_length=100)
    postal_index = models.PositiveSmallIntegerField()
    service = models.ManyToManyField(Service)
    description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.hotel_name

    def get_avg_rating(self):
        ratings = self.review_hotel.all()
        if ratings.exists():
            return round(sum(i.stars for i in ratings) / ratings.count(), 2)
        return 0

    def get_count_people(self):
        ratings = self.review_hotel.all()
        if ratings.exists():
            return ratings.count()
        return 0


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='image_hotel')
    hotel_image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return f'{self.hotel}, {self.hotel_image}'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_hotels')
    room_number = models.IntegerField()
    TYPE_ROOM = (
        ('люкс', 'люкс'),
        ('полулюкс', 'полулюкс'),
        ('эконом', 'эконом'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный')
    )
    room_type = models.CharField(max_length=25, choices=TYPE_ROOM)
    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован', 'забронирован'),
        ('занят', 'занят'),
    )
    room_status = models.CharField(max_length=60, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_description = models.TextField()

    def __str__(self):
        return f'{self.room_number}-{self.hotel}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='image_room')
    room_image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f'{self.room}, {self.room_image}'


class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel}, {self.user}'

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='review_hotel')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    stars = models.PositiveSmallIntegerField(choices= [(i, str(i)) for i in range (1, 11)])
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.hotel}, {self.user}'



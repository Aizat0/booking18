from rest_framework import serializers
from .models import (Country, UserProfile, City, Service, Hotel, HotelImage, Room, RoomImage, Booking, Review)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_image']

class CountrySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    country = CountrySimpleSerializer()
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_image', 'country']


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image']

class CitySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class HotelListSerializer(serializers.ModelSerializer):
    country = CountrySimpleSerializer()
    city = CitySimpleSerializer()
    image_hotel = HotelImageSerializer(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = ['id', 'image_hotel', 'hotel_name', 'country', 'city', 'hotel_stars', 'get_avg_rating', 'get_count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class CityDetailSerializer(serializers.ModelSerializer):
    city_hotels = HotelListSerializer(many=True, read_only=True)
    class Meta:
        model = City
        fields = ['city_name', 'city_hotels']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_name', 'service_image']


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_type', 'room_status', 'price']


class RoomDetailSerializer(serializers.ModelSerializer):
    image_room = RoomImageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['image_room', 'room_number', 'room_type', 'room_status', 'price', 'room_description']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = Review
        fields = ['id', 'user', 'comment']

class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format='%d-%m-%Y')
    class Meta:
        model = Review
        fields = ['user', 'comment', 'stars', 'created_date']

class HotelDetailSerializer(serializers.ModelSerializer):
    country = CountrySimpleSerializer()
    city = CitySimpleSerializer()
    service = ServiceSerializer(many=True)
    image_hotel = HotelImageSerializer(many=True, read_only=True)
    room_hotels = RoomListSerializer(many=True, read_only=True)
    review_hotel = ReviewListSerializer(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'image_hotel', 'country', 'city', 'hotel_stars',
                  'street', 'postal_index', 'service', 'description', 'room_hotels', 'review_hotel', 'get_avg_rating', 'get_count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


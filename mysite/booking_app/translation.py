from .models import Country, City, Service, Hotel, Room
from modeltranslation.translator import TranslationOptions,register

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)

@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('service_name',)

@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'street', 'description')

@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('room_description',)
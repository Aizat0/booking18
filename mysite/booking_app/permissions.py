from rest_framework.permissions import BasePermission

class CheckReview(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'

class CreateHotel(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'
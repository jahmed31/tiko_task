from datetime import datetime

from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user


class IsEventInFuture(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH']:
            start_date = request.data.get('start_date')
            if start_date:
                start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
                if start_date <= datetime.today().date():
                    return False
        return True

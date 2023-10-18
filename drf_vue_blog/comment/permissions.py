from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner to update'

    def saft_methods_or_owner(self, request, func):
        if request.method == SAFE_METHODS:
            return True
        
        return func()

    def has_permission(self, request, view):
        return self.saft_methods_or_owner(
            request,
            lambda: request.user.is_authenticated
        )
    
    def has_object_permission(self, request, view, obj):
        return self.saft_methods_or_owner(
            request,
            lambda: obj.author == request.user
        )

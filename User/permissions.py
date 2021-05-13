from rest_framework import permissions


class UpdatingProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # if request.method in ["GET"]:
        #     return True

        return obj.id == request.user.id


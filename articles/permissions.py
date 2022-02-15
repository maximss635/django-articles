from rest_framework import permissions


class IsPublicArticle(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return True

        return not obj.is_private


class ArticleUpdateViewPermission(IsPublicArticle):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return super(ArticleUpdateViewPermission, self).has_object_permission(request, view, obj)

        return request.user.is_superuser or obj.author == request.user

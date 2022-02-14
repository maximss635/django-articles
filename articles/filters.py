from rest_framework.filters import BaseFilterBackend


class PrivateArticleFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            return queryset
        else:
            return queryset.filter(is_private=False)


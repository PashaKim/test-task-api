
from rest_framework import filters


class BirthDateFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        birth_date = request.query_params.get('birth_date', None)
        if birth_date:
            return queryset.birth_date.filter(birth_date=birth_date)
        return queryset

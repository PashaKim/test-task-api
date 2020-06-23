
from rest_framework import filters


class BirthDateFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        birth_date = request.query_params.get('birth_date', None)
        if birth_date:
            return queryset.filter(profile__birth_date=birth_date)
        return queryset


class LocationFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        location = request.query_params.get('location', None)  # 50.9924,56.63542
        if location:
            location_l = location.split(',')
            return queryset.filter(profile__lat=float(location_l[0]), profile__lng=float(location_l[1]))
        return queryset


class RatingFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        rating = request.query_params.get('rating', None)
        if rating:
            return queryset.filter(profile__ratinge=int(rating))
        return queryset


class SexFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        sex = request.query_params.get('sex', None)  # 0 | 1 | 2
        if sex:
            return queryset.filter(profile__sex=int(sex))
        return queryset

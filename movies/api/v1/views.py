from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        qset = self.model.objects.all().values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type'
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True)
        ).annotate(
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(filmworkperson__role='actor'),
                distinct=True
            )
        ).annotate(
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(filmworkperson__role='writer'),
                distinct=True
            )
        ).annotate(
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(filmworkperson__role='director'),
                distinct=True
            )
        )
        return qset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        qset = self.get_queryset()
        paginator, page, qset, is_paginated = self.paginate_queryset(
            qset,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': len(paginator.page_range),
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(qset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.get_object()

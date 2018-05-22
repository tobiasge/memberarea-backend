from dry_rest_permissions.generics import DRYPermissionFiltersBase
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from memberarea.apps.authentication.models import User
from memberarea.apps.core.helpers import object_or_not_found
from ..models import WorkedHoursStats
from ..renderers import WorkedHoursStatsJSONRenderer
from ..serializers import WorkedHoursStatsSerializer


class WorkedHoursStatsFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        if request.user.has_perm('view_workedhoursstats'):
            return queryset
        else:
            return queryset.filter(user=request.user)


class WorkedHoursStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkedHoursStats.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = WorkedHoursStatsSerializer
    renderer_classes = (WorkedHoursStatsJSONRenderer, )
    filter_backends = (WorkedHoursStatsFilterBackend, )

    @action(methods=['GET'], detail=False, url_path='year/(?P<year>[^/.]+)')
    def year(self, request, year: int = None):
        qs_peryear = self.get_queryset().filter(year=year)
        serializer_context = {'request': request}
        page = self.paginate_queryset(qs_peryear)
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='user/(?P<userid>[^/.]+)')
    def user(self, request, userid: int = None):
        user: User = object_or_not_found(User, userid)
        qs_peruser = self.get_queryset().filter(user=user)
        serializer_context = {'request': request}
        page = self.paginate_queryset(qs_peruser)
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='year/(?P<year>[^/.]+)/user/(?P<userid>[^/.]+)')
    def yearanduser(self, request, year: int = None, userid: int = None):
        user: User = object_or_not_found(User, userid)
        qs_peryear_user = self.get_queryset().filter(user=user).filter(year=year)
        serializer_context = {'request': request}
        page = self.paginate_queryset(qs_peryear_user)
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)

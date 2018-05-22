from rest_framework.routers import DefaultRouter

from .views import (
    WorkitemViewSet, WorkitemAssignmentViewSet, WorkedHoursStatsViewSet
)

router = DefaultRouter()
router.register(r'workitems', WorkitemViewSet, base_name='workitem')
router.register(r'workitemassignments', WorkitemAssignmentViewSet, base_name='workitemassignment')
router.register(r'workedhoursstats', WorkedHoursStatsViewSet, base_name='workitemassignment')
urlpatterns = router.urls

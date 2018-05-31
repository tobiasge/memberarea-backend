from rest_framework.routers import DefaultRouter

from .views import (
    ClubhouseViewSet, RoomViewSet, DefectViewSet
)

router = DefaultRouter()
router.register(r'clubhouses', ClubhouseViewSet, base_name='clubhouse')
router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'defects', DefectViewSet, base_name='defect')
urlpatterns = router.urls

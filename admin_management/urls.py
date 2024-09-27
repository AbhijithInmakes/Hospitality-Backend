from rest_framework.routers import DefaultRouter
from .views import FacilityViewSet

router = DefaultRouter()
router.register(r'facility', FacilityViewSet, basename='facility')

urlpatterns = [
    
]


urlpatterns += router.urls

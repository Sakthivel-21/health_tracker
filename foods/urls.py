from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, FoodViewSet, FoodLogViewSet, RoutineViewSet,FoodBulkUploadAPIView

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('foods', FoodViewSet)
router.register('food-logs', FoodLogViewSet)
router.register('routines', RoutineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    path('bulk-upload/', FoodBulkUploadAPIView.as_view(), name='food-bulk-upload'),
]


    
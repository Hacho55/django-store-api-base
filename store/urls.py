from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

# URLConf
urlpatterns = router.urls


# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collection/', views.CollectionList.as_view()),
#     path('collection/<int:pk>/', views.CollectionDetail.as_view(),
#          name='collection-detail')
# ]

from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'tickets', views.TicketViewSet, basename='tickets')
router.register(r'tickets/(?P<id>\d+)/messages', views.MessagesViewSet)
urlpatterns = router.urls

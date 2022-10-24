from posixpath import basename
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register("persons", viewsets.PersonViewset, basename="persons")

urlpatterns = router.urls

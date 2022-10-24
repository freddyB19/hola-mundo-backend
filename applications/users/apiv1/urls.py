from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from applications.users.apiv1 import views

urlpatterns = [

    path("register/", views.register_user, name = "register"),
    path("register/validated/", views.validated_UsernameEmail_exists, name = "register-validated"),
    path("login/", views.login_view, name = "login"),
    path("logout/",views.logout_view, name = "logout"),



    path("api/token/", TokenObtainPairView.as_view() ,name = "obtain_token_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(),name = "obtain_refresh"),
]

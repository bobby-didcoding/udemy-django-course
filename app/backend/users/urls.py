# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.urls import path

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from users import views

app_name = "users"

urlpatterns = [
    
	##### Generic user views ######
	path('signup/',views.SignUpView.as_view(),name="signup"),
	path('activate/<uidb64>/<token>/',views.activate, name='activate'),
	path('login/',views.login_user,name="login"),
	path('logout/',views.logout,name="logout"),
	path('forgotten-password/',views.forgotten_password,name="forgotten-password"),
   
]
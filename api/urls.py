from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("transactions",views.TransactionRetrieveUpdateDestroyView,basename="transactions")

urlpatterns = [
    path("register/",views.UserCreationView.as_view()),
    
    path("categorys/",views.CategoryListCreateView.as_view()),
    
    path("categorys/<int:pk>/",views.CategoryRetrieveUpdateDestroyView.as_view()),
    
    path("categorys/summary/",views.CategoryApiView.as_view()),
    
    path("categorys/<int:pk>/transaction/add/",views.TransactionCreateView.as_view()),
    
    path("transactions/summary/",views.TransactionSummaryApiView.as_view()),
    
    path("v1/transactions", views.TransactionListView.as_view()),
    
    path("token/",ObtainAuthToken.as_view())
    
    ] +router.urls
from django.urls import path
from base import views

urlpatterns = [
    path('login/', views.loginPage, name="loginPage"),
    path('logout/', views.logoutPage, name="logoutPage"),
    path('register/', views.registerPage, name="registerPage"),
    path('',views.homePage,name="homePage"),
    path('place/<str:primaryKey>/',views.placePage,name="placePage" ),
    path('profile/<str:primaryKey>/',views.userProfile,name="userProfile" ),
    path('create-place/', views.createPlace, name="createPlace"),
    path('update-place/<str:primaryKey>/', views.updatePlace, name="updatePlace"),
    path('delete-place/<str:primaryKey>/', views.deletePlace, name="deletePlace"),
    path('delete-comment/<str:primaryKey>/', views.commentDelete, name="commentDelete"),
]

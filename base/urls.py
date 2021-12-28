from django.urls import path
from base import views

urlpatterns = [
     path('',views.homePage,name="homePage"),
     
    path('login/', views.loginPage, name="loginPage"),
    path('logout/', views.logoutPage, name="logoutPage"),
    path('register/', views.registerPage, name="registerPage"),
    path('business-register/', views.businessOwnerRegisterPage, name="businessRegisterPage"),

   
    path('place/<str:primaryKey>/',views.placePage,name="placePage" ),
    path('profile/<str:primaryKey>/',views.userProfile,name="userProfile" ),
    path('create-place/', views.createPlace, name="createPlace"),
    path('update-place/<str:primaryKey>/', views.updatePlace, name="updatePlace"),
    path('delete-place/<str:primaryKey>/', views.deletePlace, name="deletePlace"),
    path('delete-comment/<str:primaryKey>/', views.commentDelete, name="commentDelete"),
    path('update-user/', views.updateUser, name="updateUser"),
    path('contact-us/', views.contactUs, name="contactUs"),
    
    #mobile views
    path('restrictions/', views.restrictionsPage, name="restrictions"),
    path('activity/', views.activityPage, name="activityPage"),
]

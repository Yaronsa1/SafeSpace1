from django.http import response
from django.test import TestCase, Client
from .models import Room,Topic 
from django.urls import reverse,resolve
from .views import loginPage,registerPage,logoutUser,room,userProfile,createRoom,home



class TestViews(TestCase):

    def test_loginPage_GET(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_register_GET(self):
        client = Client()
        response = client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)


class TestModel(TestCase):

    def test_correct_room_created(self):
        self.room = Room.objects.create(name='test room')
        self.assertEquals(str(self.room),'test room')

    def test_correct_topic_created(self):
        self.topic = Topic.objects.create(name = 'test topic')
        self.assertEquals(str(self.topic),'test topic')
    

class TestUrls(TestCase):

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, loginPage)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)
    
    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, registerPage)
    
    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)


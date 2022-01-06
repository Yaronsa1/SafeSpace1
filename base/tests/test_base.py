from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from base.views import registerPage, placePage, userProfile, deletePlace, commentDelete, password_reset_request, \
    loginPage, logoutPage, createPlace, updatePlace, updateUser, restrictionsPage, activityPage
from mixer.backend.django import mixer

from base.models import User


class BaseTest(TestCase):

    def setUp(self):

        self.register_url=reverse('registerPage')
        self.login_url = reverse('loginPage')
        self.login_page = reverse('homePage')
        self.contact_us_url = reverse('contactUs')
        self.create_place_url = reverse('createPlace')
        self.business_register_url = reverse('businessRegisterPage')
        self.password_reset_url = reverse('password_reset')
        self.update_user= reverse('updateUser')

        self.user={
            'name':'name',
            'username':'username',
            'email':'testemail@gmail.com',
            'password1':'password',
            'password2':'password',
            'permission': '1',
            'haveBussines': True,
        }

        return super().setUp()


class egisterTest(BaseTest):


    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,200)
        # self.assertRedirects(response,self.register_url,status_code=200, target_status_code=302)

    def test_place_page(self):
        mixer.blend('base.Place')
        path = reverse('placePage', kwargs={'primaryKey': '1'})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = placePage(request, primaryKey='1')
        assert response.status_code == 200

    def test_user_profile(self):
        mixer.blend('base.User')
        path = reverse('userProfile', kwargs={'primaryKey': '1'})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = userProfile(request, primaryKey='1')
        assert response.status_code == 200


    def test_cant_delete_place(self):
        mixer.blend('base.Place')
        path = reverse('deletePlace', kwargs={'primaryKey': '1'})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = deletePlace(request, primaryKey='1')
        assert response.status_code == 200

    def test_comment_delete(self):
        mixer.blend('base.Comment')
        path = reverse('commentDelete', kwargs={'primaryKey': '1'})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = commentDelete(request, primaryKey='1')
        assert response.status_code == 200

    def test_password(self):
        mixer.blend('base.User')
        path = reverse('password_reset')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = password_reset_request(request)
        assert response.status_code == 200

    def test_create_place(self):
        mixer.blend('base.User')
        path = reverse('createPlace')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = createPlace(request)
        assert response.status_code == 200

    def test_update_place(self):
        mixer.blend('base.Place')
        path = reverse('updatePlace', kwargs={'primaryKey': '1'})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = updatePlace(request, primaryKey='1')
        assert response.status_code == 200

    def test_update_user(self):
        mixer.blend('base.User')
        path = reverse('updateUser')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = updateUser(request)
        assert response.status_code == 200

    def test_restrictions(self):
        mixer.blend('base.Restrictions')
        path = reverse('restrictions')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = restrictionsPage(request)
        assert response.status_code == 200

    def test_activity_page(self):
        mixer.blend('base.Comment')
        path = reverse('activityPage')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = activityPage(request)
        assert response.status_code == 200

    def test_can_login(self):
        response=self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code,200)

    def test_can_view_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/loginRegister.html')

    def test_can_view_home_page(self):
        response = self.client.get(self.login_page)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/homePage.html')

    def test_can_contact_us(self):
        response = self.client.get(self.contact_us_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/contactUs.html')

    def test_business_owner_can_register(self):
        response=self.client.post(self.business_register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,200)



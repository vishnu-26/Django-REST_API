from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse

from rest_framework_jwt.settings import api_settings
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

#automated new /blank db

from post.models import BlogPost
User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='xyz',email='xyz12@gmail.com')
        user_obj.set_password("12345")
        user_obj.save()
        blog_post = BlogPost.objects.create(
                    user=user_obj,
                    title='New title',
                    content='some_random_content')



    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count,1)

    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count,1)


    def test_get_list(self):
        data= {}
        url = api_reverse("api-posts:post-listcreate")
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_post_item(self):
        user_obj =  User.objects.first()
        data= {"user":user_obj.id,"title":" Restapi Testing","content":"MY First API testing"}
        url = api_reverse("api-posts:post-listcreate")
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
#
    def test_get_item(self):
        data= {}
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        print(url)
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print(response.data)

    def test_update_item(self):
        data= {"title": "Testing","content": "MY First API testing"}
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_update_item_with_user(self):
        data= {"title": "Good Evening",
                "content": "Started rest api"}
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        print(blog_post.content)
        print(blog_post.user)
        print(blog_post.user.email)
        user_obj =  User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        print(user_obj)
        print(url)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.patch(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print(BlogPost.objects.first().content)


    



    def test_post_item_with_user(self):
        url = api_reverse("api-posts:post-listcreate")
        user_obj =  User.objects.first()
        data= {"user":user_obj.id,"title": "Testing",
                "content": "ReST api testing"}
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        print(user_obj)
        print(url)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    

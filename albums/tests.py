from django.test import TestCase

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Album


class AlbumModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_album = Album.objects.create(
            author = test_user,
            title = 'Moonflowers',
            band = 'Swallow The Sun',
            rating = 8,
            description = 'Sad'
        )
        test_album.save()

    def test_album_content(self):
        album = Album.objects.get(id=1)

        self.assertEqual(str(album.author), 'tester')
        self.assertEqual(album.title, 'Moonflowers')
        self.assertEqual(album.band, 'Swallow The Sun')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('album_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # NOTE: TIME STAMP MAKES IT UNCONVENTIONAL TO TEST THIS WITHOUT USING OTHER TOOLS OR WORKAROUNDS 
    
    # def test_detail(self):

    #     test_user = get_user_model().objects.create_user(username='tester',password='pass')
    #     test_user.save()

    #     test_album = Album.objects.create(
    #         author = test_user,
    #         title = 'Moonflowers',
    #         band = 'Swallow The Sun',
    #         rating = 8,
    #         description = 'Sad',
    #     )
    #     test_album.save()

    #     response = self.client.get(reverse('album_detail', args=[1]))

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, {
    #         'id':1,
    #         'title': test_album.title,
    #         'band': test_album.band,
    #         'rating' : test_album.rating,
    #         'description' : test_album.description,            
    #         'author': test_user.id,
    #         'created' : test_album.created,
    #         'updated' : test_album.updated,
    #     })


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        url = reverse('album_list')
        data = {
            "title":"Testing is NOT Fun!!!",
            "band":"everybody",
            'rating' : 1,
            'description' : 'Very sad', 
            "author":test_user.id,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Album.objects.count(), 1)
        self.assertEqual(Album.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_album = Album.objects.create(
            author = test_user,
            title = 'Moonflowers',
            band = 'Swallow The Sun'
        )

        test_album.save()

        url = reverse('album_detail',args=[test_album.id])
        data = {
            "title":"Testing is Still NOT Fun!!!",
            "author":test_album.author.id,
            "band":test_album.band,
            'rating' : 1,
            'description' : 'Very sad', 
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Album.objects.count(), test_album.id)
        self.assertEqual(Album.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a album."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_album = Album.objects.create(
            author = test_user,
            title = 'Moonflowers',
            band = 'Swallow The Sun'
        )

        test_album.save()

        album = Album.objects.get()

        url = reverse('album_detail', kwargs={'pk': album.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)

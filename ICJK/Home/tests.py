from django.test import TestCase
from django.urls import reverse

#from .models import

# Create your tests here.

class PersonalHomeViewTest(TestCase):

    def test_no_search(self):
        #response = self.client.get(reverse('Home'))

        response = self.client.get('/personal')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cars here")
        self.assertQuerysetEqual(response.context['carlist'], [])

    def test_toyota(self):
        response = self.client.get('/personal?query=Toyota&viewtype=personal&action=submit')
        self.assertEqual(response.status_code, 200)
        #change after connecting database
        self.assertContains(response, "Toyota Yaris")
        self.assertEqual(len(response.context['carlist']), 4)

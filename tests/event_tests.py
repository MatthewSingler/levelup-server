from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from levelupapi.models import Event, EventGamer


class EventTests(APITestCase):
    def setUp(self):
        # Define the URL path for registering a Gamer
        url = '/register'

        # Define the Gamer properties
        gamer = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        response = self.client.post(url, gamer, format='json')
        self.token = Token.objects.get(pk=response.data['token'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        event = Event()
        event.game = "Test game"
        event.save()

    def test_create_event(self):
        url = "/events"
        event = {
            "game": "Mouse Trap",
            "description": "Dont get caught",
            "date": "2021-12-01",
            "time": "12:00:00",
            "organizer": "Gamer?"
        }
        response = self.client.post(url, event, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["gamer"]['user'], self.token.user_id)
        self.assertEqual(response.data["game"], event['game'])
        self.assertEqual(response.data["description"], event['description'])
        self.assertEqual(response.data["date"], event['date'])
        self.assertEqual(response.data["time"], event['time'])
        self.assertEqual(response.data["organizer"]['id'], event['organizer'])

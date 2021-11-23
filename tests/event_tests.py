from django.http import request, response
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from levelupapi.models import Event, EventGamer, Game, Gamer, GameType


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
        game_type = GameType()
        game_type.label = "action game"
        game_type.save()
        self.game = Game.objects.create(
            game_type = game_type,
            title = "action game",
            maker = "hasbro",
            gamer_id = 1,
            number_ofPlayers = 4,
            skill_level = 2
        )

    def test_retrieve(self):
        event = Event.objects.create(
            organizer_id = 1,
            game = self.game,
            time = "12:00:00",
            date = "2021-12-21",
            description = "A fun game"
        )
        url = f"/events/{event.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], event.id)
        self.assertEqual(response.data['organizer']['id'], event.organizer.id)
        self.assertEqual(response.data['date'], event.date)
        self.assertEqual(response.data['time'], event.time)
        self.assertEqual(response.data['description'], event.description)
        
    def test_create(self):
        event = {
            "date": "2021-12-21",
            "time": "12:00:00",
            "description": "Fun times",
            "gameId": self.game.id
        }
        response = self.client.post('/events',event, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])
        self.assertEqual(response.data['organizer']['id'], event.organizer.id)
        self.assertEqual(response.data['date'], event['date'])
        self.assertEqual(response.data['time'], event['time'])
        self.assertEqual(response.data['description'], 1)

    #def test_get_event(self):
        

    def test_delete(self):
        event = Event.objects.create(
            organizer_id=1,
            game=self.game,
            time="12:00:00",
            date="2021-12-21",
            description="A fun game"
        )
        response = self.client.delete(f'/events/{event.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        get_response = self.client.get(f'/events/{event.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

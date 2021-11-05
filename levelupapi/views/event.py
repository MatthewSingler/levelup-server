from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, EventGamer, event_gamer, Game, Gamer, gamer
from levelupapi.views.game import GameSerializer
from rest_framework import status
from django.core.exceptions import ValidationError


class EventView(ViewSet):

    def list(self, request):
        events = Event.objects.all()
        game = self.request.query_params.get("game", None)
        gamer = Gamer.objects.get(user=request.auth.user)
        if game is not None:
            events = events.filter(game__id=game)

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        event = Event.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=gamer,
            game=game
            )
        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

"""def retrieve(self, request, pk=None)
    event = Event.objects.get(pk=pk)
    event_serializer = EventSerializer(event, context={"request": request})
    return Response(event_serializer.data)

def destroy(self, request, pk)
    event = Event.objects.get(pk=pk)
    event.delete()

def update(self, request, pk)
    event = Event.objects.get(pk=pk)
    event.date = request.data["date"]
    """


class EventGamerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ("user", "bio")

class EventSerializer(serializers.ModelSerializer):
    organizer = EventGamerSerializer()
    game = GameSerializer()


    class Meta:
        model = Event
        fields = ("id", "game", "organizer", "description", "date", "time")

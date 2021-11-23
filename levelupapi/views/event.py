from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, EventGamer, event_gamer, Game, Gamer
from levelupapi.views.game import GameSerializer
from rest_framework.serializers import ModelSerializer, BooleanField, CharField
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from django.contrib.auth.models import User


class EventView(ViewSet):

    def list(self, request):
        events = Event.objects.all()
        game = self.request.query_params.get("game", None)
        gamer = Gamer.objects.get(user=request.auth.user)
        for event in events:
            event.joined = gamer in event.attendees.all()
        if game is not None:
            events = events.filter(game__id=game)

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        game = Game.objects.get(pk=request.data["game"])
        gamer = Gamer.objects.get(user=request.auth.user)
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

    def retrieve(self, request, pk)
        try:
            event = Event.objects.get(pk=pk)
            event_serializer = EventSerializer(event, context={"request": request})
            return Response(event_serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message', 'event not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk)
        event = Event.objects.get(pk=pk)
        event.delete()

    def update(self, request, pk)
        event = Event.objects.get(pk=pk)
        event.date = request.data["date"]


    @action(methods=['post', 'delete'], detail=True)
        def signup(self, request, pk=None):
        """Managing gamers signing up for events"""
        # Django uses the `Authorization` header to determine
        # which user is making the request to sign up
        gamer = Gamer.objects.get(user=request.auth.user)
        try:
            # Handle the case if the client specifies a game
            # that doesn't exist
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {'message': 'Event does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A gamer wants to sign up for an event
        if request.method == "POST":
            try:
                # Using the attendees field on the event makes it simple to add a gamer to the event
                # .add(gamer) will insert into the join table a new row the gamer_id and the event_id
                event.attendees.add(gamer)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined event
        elif request.method == "DELETE":
            try:
                # The many to many relationship has a .remove method that removes the gamer from the attendees list
                # The method deletes the row in the join table that has the gamer_id and event_id
                event.attendees.remove(gamer)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})


class EventGamerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ("user", "id")

class EventSerializer(serializers.ModelSerializer):
    organizer = EventGamerSerializer()
    game = GameSerializer()
    joined = serializers.BooleanField(required=False)


    class Meta:
        model = Event
        fields = ("id", "game", "organizer", "description", "date", "time", "joined")

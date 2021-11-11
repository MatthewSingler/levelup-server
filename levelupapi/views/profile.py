from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from levelupapi.models import Gamer, Event, Game
from rest_framework import serializers
from django.contrib.auth.models import User


@api_view(['GET'])
def user_profile(request):
    """Handle GET requests to profile resource

    Returns:
        Response -- JSON representation of user info and events
    """
    gamer = Gamer.objects.get(user=request.auth.user)

    # TODO: Use the django orm to filter events if the gamer is attending the event
    #attending = Event.objects.filter(attendees=gamer)
    #or
    attending = gamer.attending.all()

    # TODO: Use the orm to filter events if the gamer is hosting the event
    #hosting = Event.objects.filter(organizer=gamer)
    #or
    hosting = gamer.event_set

    attending_serialized = EventSerializer(attending, many=True, context={'request': request})
    hosting_serialized = EventSerializer(hosting, many=True, context={'request': request})
    gamer_serialized = GamerSerializer(gamer)

    # Manually construct the JSON structure you want in the response
    response = {
        "gamer": gamer_serialized.data,
        "attending": attending_serialized.data,
        "hosting": hosting_serialized.data
    }

    return Response(response)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', 'bio')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('title',)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time')

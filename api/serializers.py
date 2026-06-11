from rest_framework.serializers import ModelSerializer, SerializerMethodField
from base.models import Room, Topic, User, Message
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'avatar_url']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class RoomSerializer(ModelSerializer):
    host = UserSerializer(read_only=True)
    topic = TopicSerializer(required=False, read_only=True)
    topic_name = serializers.CharField(write_only=True, required=False)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Room    
        fields = '__all__'
        read_only_fields = [
            'participants',
        ]

    def get_message_count(self, obj):
        return obj.room_messages.count()

    def create(self, validated_data):
        topic_name = validated_data.pop('topic_name', None)
        
        if topic_name:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            validated_data['topic'] = topic
            
        return Room.objects.create(**validated_data)
    


class RoomSummarySerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name'] 


class MessageSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    room_details = RoomSummarySerializer(source='room', read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'user', 'room', 'room_details', 'body', 'created', 'updated']
        read_only_fields = ['id', 'user', 'created', 'updated']
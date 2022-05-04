from django.contrib.auth import get_user_model
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        ModelSerializer, SerializerMethodField)

from tickets.models import Messages, Tickets


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id', 'email', 'password', 'name', 'support')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)


class MessagesSerializer(ModelSerializer):
    replys = SerializerMethodField()

    def get_replys(self, obj):
        queryset = Messages.objects.filter(parent_id=obj.id)
        serializer = MessagesSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Messages
        fields = ('user', 'content', 'replys')


class TicketListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='tickets-detail')
    client = SerializerMethodField(read_only=True)
    support_ticket = SerializerMethodField(read_only=True)

    def get_client(self, obj):
        return str(obj.client)

    def get_support_ticket(self, obj):
        return str(obj.support_ticket)

    class Meta:
        model = Tickets
        fields = ('url', 'title', 'text', 'client', 'support_ticket', 'status')


class TicketDetailSerializer(ModelSerializer):
    client = SerializerMethodField(read_only=True)
    messages = SerializerMethodField()

    def get_client(self, obj):
        return str(obj.client.email)

    def get_messages(self, obj):
        queryset = Messages.objects.filter(ticket_id=obj.id, parent_id=None)
        serializer = MessagesSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Tickets
        fields = ('url', 'title', 'text', 'client', 'status', 'messages')
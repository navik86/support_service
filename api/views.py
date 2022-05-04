from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (MessagesSerializer, TicketDetailSerializer,
                             TicketListSerializer, UserSerializer)
from tickets.models import Messages, Tickets


class UserViewSet(ModelViewSet):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class TicketViewSet(ModelViewSet):
    model = Tickets
    queryset = model.objects.none()
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        return TicketDetailSerializer

    def get_queryset(self):
        if self.request.user.admin:
            return self.model.objects.all()
        return self.model.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
        serializer.save()


class MessagesViewSet(ModelViewSet):
    model = Messages
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    def get_queryset(self):
        ticket_id = self.kwargs["id"]
        queryset = Messages.objects.filter(ticket_id=ticket_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
        serializer.save()
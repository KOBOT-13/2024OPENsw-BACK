from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import QuizRecord

class QuizRecordViewSet(viewsets.ModelViewSet):
    queryset = QuizRecord.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return QuizRecord.objects.filter(user=user).select_related('book').order_by('-completed_at')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return QuizRecordSerializer
        return QuizRecordCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
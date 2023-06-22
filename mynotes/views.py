from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import NotesSerializer
from .models import Notes

class NotesView(APIView):
    permission_classes = (IsAuthenticated,)
    print("NotesView")
    # def get(self, request):
    #     notes = Notes.objects.filter(user=request.user)
    #     serializer = NotesSerializer(notes, many=True)
    #     return Response(serializer.data)
    
    
    def post(self, request):
        serializer = NotesSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            serializer.save(user=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

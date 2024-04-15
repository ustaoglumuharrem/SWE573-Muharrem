from django.shortcuts import render
from rest_framework import generics
from .models import UserCommunityy
from .serializers import UserCommunityySerializer

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



class UserCommunityyView(generics.GenericAPIView):  

    def get(self, request):  
        result = UserCommunityy.objects.all() 
        serializer_class = UserCommunityySerializer(result,many=True)  
        return Response({'success': 'success', "students":serializer_class.data}, status=200) 
        
  
    def post(self, request):  
        serializer_class = UserCommunityySerializer(data=request.data)  
        if serializer_class.is_valid():  
            serializer_class.save()  
            return Response({"status": "success", "data": serializer_class.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)  
  
    def patch(self, request, id):  
        result = UserCommunityy.objects.get(id=id)  
        serializer_class = UserCommunityySerializer(result, data = request.data, partial=True)  
        if serializer_class.is_valid():  
            serializer_class.save()  
            return Response({"status": "success", "data": serializer_class.data})  
        else:  
            return Response({"status": "error", "data": serializer_class.errors})  
  
    def delete(self, request, id=None):  
        result = get_object_or_404(UserCommunityy, id=id)  
        result.delete()  
        return Response({"status": "success", "data": "Record Deleted"})
    

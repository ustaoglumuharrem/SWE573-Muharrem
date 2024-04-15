
from rest_framework import generics
from .models import CommunityTemplate
from .serializers import CommunityTemplateSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



class CommunityTemplateView(generics.GenericAPIView):  

    def get(self, request):  
        result = CommunityTemplate.objects.all() 
        serializer_class = CommunityTemplateSerializer(result,many=True)  
        return Response({'success': 'success', "students":serializer_class.data}, status=200) 
        
  
    def post(self, request):  
        serializer_class = CommunityTemplateSerializer(data=request.data) 
        if serializer_class.is_valid():  
            serializer_class.save()
            return Response({"status": "success", "data": serializer_class.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)  
  
    def patch(self, request, id):  
        result = CommunityTemplate.objects.get(id=id)  
        serializer_class = CommunityTemplateSerializer(result, data = request.data, partial=True)  
        if serializer_class.is_valid():  
            serializer_class.save()  
            return Response({"status": "success", "data": serializer_class.data})  
        else:  
            return Response({"status": "error", "data": serializer_class.errors})  
  
    def delete(self, request, id=None):  
        result = get_object_or_404(CommunityTemplate, id=id)  
        result.delete()  
        return Response({"status": "success", "data": "Record Deleted"})
    

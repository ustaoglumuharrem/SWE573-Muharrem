# myapp/views.py
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from .serializers import UserPasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class UserView(generics.GenericAPIView):  
    authentication_classes = [TokenAuthentication]  # Use TokenAuthentication for authentication
    permission_classes = [IsAuthenticated]  # Require authentication for all methods

    def get(self, request):  
        result = User.objects.all() 
        serializer_class = UserSerializer(result,many=True)  
        return Response({'success': 'success', "students":serializer_class.data}, status=200) 
        
  
    def post(self, request):  
        serializer_class = UserSerializer(data=request.data) 
        if serializer_class.is_valid():  
            serializer_class.save()
            return Response({"status": "success", "data": serializer_class.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)  
  
    def patch(self, request, id):  
        result = User.objects.get(id=id)  
        serializer_class = UserSerializer(result, data = request.data, partial=True)  
        if serializer_class.is_valid():  
            serializer_class.save()  
            return Response({"status": "success", "data": serializer_class.data})  
        else:  
            return Response({"status": "error", "data": serializer_class.errors})  
  
    def delete(self, request, id=None):  
        result = get_object_or_404(User, id=id)  
        result.delete()  
        return Response({"status": "success", "data": "Record Deleted"})
    
class UserPasswordView(generics.GenericAPIView): 
    authentication_classes = [TokenAuthentication]  # Use TokenAuthentication for authentication
    permission_classes = [IsAuthenticated]  # Require authentication for all methods 
    def post(self, request):
          
        serializer_class = UserPasswordSerializer(data=request.data)  
        
        if serializer_class.is_valid():
            username = serializer_class.validated_data['userName']
            password = serializer_class.validated_data['password']  
            try:
                user = User.objects.get(userName=username)
                if UserPasswordView.check_password(user,password):
                    return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def check_password(user,password):
        if user.password==password:
            return True
        else:
            return False  

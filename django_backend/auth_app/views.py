from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from .wrappers import header_checker

from .serializers import LoginSerializer, SignupSerializer

class SignupAPIView(APIView):
    def post(self,request):
            serializer = SignupSerializer(data = request.data)
            if serializer.is_valid():
                    serializer.save()
                    token = Token.objects.create(user=serializer.instance)
                    res = { 'status' : status.HTTP_201_CREATED }
                    return Response(res, status = status.HTTP_201_CREATED)
            res = { 'status' : status.HTTP_400_BAD_REQUEST, 'data' : serializer.errors }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self,request):
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                    username = serializer.validated_data["username"]
                    password = serializer.validated_data["password"]
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        token, _ = Token.objects.get_or_create(user=user)
                        response = {
                               "status": status.HTTP_200_OK,
                               "message": "success",
                               "data": {
                                       "Token" : token.key
                                       }
                               }
                        return Response(response, status = status.HTTP_200_OK)
                    else :
                        response = {
                               "status": status.HTTP_401_UNAUTHORIZED,
                               "message": "Invalid Username or Password",
                               }
                        return Response(response, status = status.HTTP_401_UNAUTHORIZED)
            response = {
                 "status": status.HTTP_400_BAD_REQUEST,
                 "message": "bad request",
                 "data": serializer.errors
                 }
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
    

class LogoutAPIView(APIView):
      def post(self, request):
            # print(request.__dict__)
            # print(request.headers)
            if 'Authorization' not in request.headers:
                return Response({"Data": "Unauthorized"}, status=401)
            
            try:
                token = request.headers['Authorization'].split(' ', 1)[1]
                dbToken=Token.objects.get(key=token)
                dbToken.delete()
            except Exception as e:
                print(e)
                return Response("Error", status=400)
                 
                  

            print(token)
            return Response({})
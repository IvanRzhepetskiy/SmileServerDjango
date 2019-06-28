import traceback

from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.
from App.models import Recognition


class LoginToken(APIView):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    renderer_classes = [renderers.JSONRenderer]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).exists():
                user = User.objects.get(username=username)
                #user1 = auth.authenticate(username=username, password=password)
                if not user.check_password(password):
                    return Response({'success': False, 'message': 'Password incorrect'})
                if Token.objects.filter(user=user).exists():
                    token = Token.objects.get(user=user)
                    return Response({'success': True, 'token': token.key})
                else:
                    token = Token.objects.create(user=user)
                    return Response({'success': True, 'token': token.key})
            return Response({'success': False, 'message': 'User doesn\'t exists'})
        except Exception:
            traceback.print_exc()
            return Response({'success': False})


class Register(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def post(self, request):
        username = request.data.get('username')
        login = request.data.get('login')
        password = request.data.get('password')

        try:
            if not User.objects.filter(username = login).exists():
                User.objects.create_user(username=login,first_name=username, password=password)
                #user.profile.bio = 'Something about me'
            else:
                return Response({'success': False , 'message' : 'login already exists'})
            return Response({'success': True})
        except Exception:
            traceback.print_exc()
            return Response({'success': False})

class AddRecognition(APIView):
    renderer_classes = [renderers.JSONRenderer]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.data.get('Token')
        time = request.data.get('time')
        print(time)
        if Token.objects.filter(key = token).exists():
            token = Token.objects.get(key = token)
            rec = Recognition(user=token.user, time=time)
            rec.save()
            return Response({'success': True})
        else:
            return Response({'success': False, 'message' : 'Token is incorrect'})
        return Response({'success': False})
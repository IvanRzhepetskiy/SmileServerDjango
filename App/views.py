import traceback

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.



class LoginToken(APIView):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    renderer_classes = [renderers.JSONRenderer]

    def post(self, request):
        login = request.data.get('login')
        print(login)
        password = request.data.get('password')

        try:
            if User.objects.filter(username = login).exists():
                user = User.objects.get(username=login)
                if Token.objects.filter(user=user).exists():
                    token = Token.objects.get(user=user)
                    return Response({'success': True, 'token': token.key})
                else:
                    token = Token.objects.create(user=user)
                    return Response({'success': True, 'token': token.key})
            return Response({'success': True, 'token': 'User doesn\'t exists'})
        except Exception:
            traceback.print_exc()
            return Response({'success': False})


class Register(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def post(self, request):
        login = request.data.get('login')
        print(login)
        password = request.data.get('password')

        try:
            if User.objects.filter(username = login).exists():
                user = User.objects.get(username=login)
                if Token.objects.filter(user=user).exists():
                    token = Token.objects.get(user=user)
                    return Response({'success': True, 'token': token.key})
                else:
                    token = Token.objects.create(user=user)
                    return Response({'success': True, 'token': token.key})
            return Response({'success': True, 'token': 'User doesn\'t exists'})
        except Exception:
            traceback.print_exc()
            return Response({'success': False})
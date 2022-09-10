import datetime

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views import View
from knox.models import AuthToken
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework import status, generics
from rest_framework.response import Response
from django.conf import settings
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from random import choices
from knox.views import LoginView as KnoxLoginView


# Create your views here.

class ShortenerListAPIView(ListAPIView):
    queryset = Link.objects.filter(private=False)
    serializer_class = LinkSerializer1


class ShortenerCreateApiView(CreateAPIView):
    serializer_class = LinkSerializer


class Redirector(APIView):
    def get(self, request, shortener_link, *args, **kwargs):
        shortener_link = settings.HOST_URL + '/' + self.kwargs['shortener_link']
        redirect_link = Link.objects.filter(shortened_link=shortener_link).first().original_link
        exp_date = Link.objects.filter(shortened_link=shortener_link).first().expiration_date
        # if datetime.datetime.now() > exp_date:
        return redirect(redirect_link)
        # return Response({"Message": "Link is expired"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)
        url = Link.objects.filter(user=user)
        link_serializer = LinkSerializer(url, many=True)
        number_of_link = Link.objects.filter(user=user).count()

        return Response({'user': serializer.data,
                         'number_of_link':number_of_link,
                         'link': link_serializer.data},
                        status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

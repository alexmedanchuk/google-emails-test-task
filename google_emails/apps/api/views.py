import oauth2client

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .utils import EmailsRetriever


class ListUsers(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        social = request.user.social_auth.filter(provider='google-oauth2')[0]
        access_token = social.extra_data['access_token']
        retriever = EmailsRetriever(access_token, request.user.email)

        try:
            messages = retriever.retrieve()
        except oauth2client.client.AccessTokenCredentialsError as err:
            return Response({'error': 'Authentication error'}, status=status.HTTP_403_FORBIDDEN)

        return Response(messages)

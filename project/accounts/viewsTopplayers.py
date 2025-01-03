from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import UserProfile
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer

class TopPlayersView(APIView):
    permission_classes = [AllowAny]  # Allow public access to this endpoint

    def get(self, request):
        top_players = UserProfile.objects.order_by('-level')[:10]  # Get top 10 players by level
        serializer = UserProfileSerializer(top_players, many=True)
        return Response(serializer.data, status=200)



class UserInGame(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, result):

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        user_profile = UserProfile.objects.get(user__id=user_id)
        if result == "true":
            user_profile.inGame = True
        elif result == "false":
            user_profile.inGame = False
        else:
            return Response({"error": "Invalid result. Use 'false' or 'true'."}, status=400)
        user_profile.save()
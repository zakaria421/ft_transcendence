from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
#*********************************************************************new
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import UserProfile

from django.views.decorators.csrf import csrf_exempt
import json

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            # Get the UserProfile related to this user
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        # Serialize the UserProfile data
        serializer = UserProfileSerializer(user_profile)

        # Return the serialized data
        return Response(serializer.data, )

@csrf_exempt

def add_friend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        if not username:
            return JsonResponse({"success": False, "error": "Username is required."}, status=400)

        try:
            # Find the friend to add
            friend_user = User.objects.get(username=username)
            friend_profile = UserProfile.objects.get(user=friend_user)

            # Get the current user's profile
            current_user_profile = UserProfile.objects.get(user=request.user)

            # Add the friend
            current_user_profile.friends.add(friend_user)

            return JsonResponse({"success": True, "message": f"{username} added as a friend!"})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request."}, status=400)


def search_friends(request):
    query = request.GET.get('query', '').strip()
    print(f"Search query received: {query}")
    print(f"User: {request.user}")

    if query:
        # Include the logged-in user's profile in the search
        user_profiles = UserProfile.objects.filter(
            Q(nickname__icontains=query) | Q(email__icontains=query)
        ).distinct()[:10]  # Avoid duplicates and limit results to 10
        
        print(f"Found {len(user_profiles)} profiles")
        
        results = [
            {
                "id": profile.user.id,
                "name": profile.nickname,
                "avatar": profile.profile_picture.url if profile.profile_picture else "",
                "bio": profile.bio,
                "is_self": profile.user == request.user,  # Indicate if it's the logged-in user
            }
            for profile in user_profiles
        ]
        
        return JsonResponse({"results": results}, status=200)
    
    return JsonResponse({"results": []}, status=200)

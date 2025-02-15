from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/',                    include('accounts.urls')),
    # path('api/',                include('accounts.urls')),
    path('admin/',              admin.site.urls),
    path('api/friends/',            include('friendship.urls')),
    path('api/smartcontract/',      include('SmartContract.urls')),
    path('api/token/',          TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',  TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/',   TokenVerifyView.as_view(), name='token_verify'),


] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
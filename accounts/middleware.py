from django.shortcuts import redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class RoleBasedRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to handle role-based redirects after login
    """
    def process_response(self, request, response):
        return response

class AuthenticationRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to redirect authenticated users away from login/register pages
    """
    def process_request(self, request):
        # Don't redirect if user is not authenticated
        if not request.user.is_authenticated:
            return None

        # URLs that authenticated users should not access
        restricted_urls = ['/accounts/login/', '/accounts/register/']

        if request.path in restricted_urls:
            # Redirect based on user role
            if request.user.is_owner():
                return redirect('accounts:owner_dashboard')
            elif request.user.is_pegawai():
                return redirect('accounts:pegawai_dashboard')
            else:
                return redirect('home')

        return None
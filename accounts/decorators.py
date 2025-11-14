from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def pegawai_required(view_func):
    """
    Decorator to ensure user is logged in and has pegawai role
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Anda harus login terlebih dahulu.')
            return redirect('accounts:login')

        if not request.user.is_pegawai():
            messages.error(request, 'Akses ditolak. Halaman ini hanya untuk pegawai.')
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def owner_required(view_func):
    """
    Decorator to ensure user is logged in and has owner role
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Anda harus login terlebih dahulu.')
            return redirect('accounts:login')

        if not request.user.is_owner():
            messages.error(request, 'Akses ditolak. Halaman ini hanya untuk owner.')
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def pegawai_or_owner_required(view_func):
    """
    Decorator to ensure user is logged in and has either pegawai or owner role
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Anda harus login terlebih dahulu.')
            return redirect('accounts:login')

        if not (request.user.is_pegawai() or request.user.is_owner()):
            messages.error(request, 'Akses ditolak. Anda tidak memiliki hak akses.')
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return _wrapped_view
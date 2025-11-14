from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import CustomAuthenticationForm, EmployeeRegistrationForm
from .models import User
from orders.models import Order
from customers.models import Customer
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Login berhasil! Selamat datang, {user.get_full_name() or user.username}.")

                # Redirect based on user role
                next_url = request.GET.get('next', get_dashboard_url(user))
                return redirect(next_url)
            else:
                messages.error(request, 'Username atau password salah.')
        else:
            messages.error(request, 'Username atau password salah.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'Anda telah keluar dari sistem.')
    return redirect('accounts:login')

@login_required
def pegawai_dashboard(request):
    """Dashboard for Pegawai role"""
    # Only allow pegawai role, not owner
    if not request.user.is_pegawai():
        messages.error(request, 'Akses ditolak. Halaman ini hanya untuk pegawai.')
        return redirect('accounts:owner_dashboard' if request.user.is_owner() else 'home')

    # Get dashboard statistics
    today = timezone.now().date()

    # Orders statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status__in=['diterima', 'proses']).count()
    today_orders = Order.objects.filter(date_received=today).count()
    completed_orders = Order.objects.filter(status='selesai').count()

    # Recent orders
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:5]

    # Overdue orders
    overdue_orders = Order.objects.filter(
        status__in=['diterima', 'proses'],
        estimated_completion__lt=today
    )[:3]

    context = {
        'page_title': 'Dashboard Pegawai',
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'today_orders': today_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
        'overdue_orders': overdue_orders,
        'user_role': 'pegawai'
    }

    return render(request, 'accounts/dashboard_pegawai.html', context)

@login_required
def owner_dashboard(request):
    """Dashboard for Owner role"""
    if not request.user.is_owner():
        messages.error(request, 'Akses ditolak. Anda bukan owner.')
        return redirect('home')

    # Get all pegawai dashboard stats
    today = timezone.now().date()

    # Orders statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status__in=['diterima', 'proses']).count()
    today_orders = Order.objects.filter(date_received=today).count()
    completed_orders = Order.objects.filter(status='selesai').count()

    # Financial statistics
    total_revenue = Order.objects.aggregate(total=Sum('total_cost'))['total'] or 0
    today_revenue = Order.objects.filter(date_received=today).aggregate(total=Sum('total_cost'))['total'] or 0

    # Customer statistics
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()

    # Employee statistics
    total_employees = User.objects.filter(role='pegawai').count()
    active_employees = User.objects.filter(role='pegawai', is_active=True).count()

    # Recent orders
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:10]

    # Overdue orders
    overdue_orders = Order.objects.filter(
        status__in=['diterima', 'proses'],
        estimated_completion__lt=today
    )[:5]

    context = {
        'page_title': 'Dashboard Owner',
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'today_orders': today_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'total_customers': total_customers,
        'active_customers': active_customers,
        'total_employees': total_employees,
        'active_employees': active_employees,
        'recent_orders': recent_orders,
        'overdue_orders': overdue_orders,
        'user_role': 'owner'
    }

    return render(request, 'accounts/dashboard_owner.html', context)

def get_dashboard_url(user):
    """Get dashboard URL based on user role"""
    if user.is_owner():
        return 'accounts:owner_dashboard'
    elif user.is_pegawai():
        return 'accounts:pegawai_dashboard'
    return 'home'

@login_required
@require_POST
def create_employee(request):
    """Create new employee (AJAX endpoint for owner)"""
    if not request.user.is_owner():
        return JsonResponse({'success': False, 'error': 'Akses ditolak'})

    form = EmployeeRegistrationForm(request.POST)
    if form.is_valid():
        try:
            employee = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Pegawai {employee.get_full_name()} berhasil ditambahkan.',
                'employee': {
                    'id': employee.id,
                    'name': employee.get_full_name(),
                    'username': employee.username,
                    'email': employee.email,
                    'phone': employee.phone_number,
                    'is_active': employee.is_active
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': form.errors})

def home(request):
    """Home page with login and status check options"""
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))

    return render(request, 'home.html')

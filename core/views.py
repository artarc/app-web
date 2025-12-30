from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	return render(request, 'core/index.html')


@staff_member_required
def dashboard(request, variation=None):
	context = {'variation': variation}
	return render(request, 'core/dashboard.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


def _add_input_classes(form, autofocus=None):
	"""Adiciona classes Tailwind aos widgets dos campos do form."""
	css = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm p-2"
	for name, field in form.fields.items():
		attrs = field.widget.attrs
		# preserve existing attrs
		attrs.setdefault('class', css)
		field.widget.attrs = attrs
	if autofocus and autofocus in form.fields:
		form.fields[autofocus].widget.attrs['autofocus'] = 'autofocus'


def index(request):
	# Always show the index page; do not force redirect authenticated users to dashboard
	return render(request, 'core/index.html')


@login_required
def dashboard(request, variation=None):
	context = {'variation': variation}
	return render(request, 'core/dashboard.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')


# Registration form with email
class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta(UserCreationForm.Meta):
		fields = ('username', 'email')

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


def auth_login(request):
	"""Combined login page that shows both login and register forms.
	Handles login POST; registration POST goes to `register`.
	"""
	if request.method == 'POST':
		login_form = AuthenticationForm(request, data=request.POST)
		reg_form = RegistrationForm()
		_add_input_classes(login_form, autofocus='username')
		_add_input_classes(reg_form)
		if login_form.is_valid():
			user = login_form.get_user()
			login(request, user)
			# session expiration: respect "remember" checkbox
			if request.POST.get('remember'):
				# two weeks
				request.session.set_expiry(1209600)
			else:
				# expire on browser close
				request.session.set_expiry(0)
			# ensure session is saved
			request.session.save()
			return redirect('index')
	else:
		login_form = AuthenticationForm()
		reg_form = RegistrationForm()
		_add_input_classes(login_form, autofocus='username')
		_add_input_classes(reg_form)

	return render(request, 'registration/login.html', {'login_form': login_form, 'reg_form': reg_form})


def register(request):
	# GET: show registration page; POST: process registration
	if request.method == 'POST':
		reg_form = RegistrationForm(request.POST)
		_add_input_classes(reg_form)
		if reg_form.is_valid():
			user = reg_form.save()
			raw_password = reg_form.cleaned_data.get('password1')
			user = authenticate(request, username=user.username, password=raw_password)
			if user is not None:
				login(request, user)
				# keep newly registered users logged for two weeks
				request.session.set_expiry(1209600)
				request.session.save()
				return redirect('dashboard')
			# fallback
			return redirect('login')
		# invalid: re-render register page with errors
		return render(request, 'registration/register.html', {'reg_form': reg_form})
	else:
		reg_form = RegistrationForm()
		_add_input_classes(reg_form, autofocus='username')
		return render(request, 'registration/register.html', {'reg_form': reg_form})

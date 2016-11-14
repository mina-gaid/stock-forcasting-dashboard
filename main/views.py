from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def login(request):
    return render(request, 'main/login.html')
	
def logout(request):
    return render(request, 'main/index.html')

def preset(request):
    return render(request, 'main/password-reset.html')

def signup(request):
    return render(request, 'main/signup.html')

def support(request):
    return render(request, 'main/faq.html')

def contact(request):
    return render(request, 'main/contact.html')

def terms(request):
    return render(request, 'main/terms-and-conditions.html')

class UserFormView(View):
	form_class = UserForm
	template_name = 'main/signup.html'

	# display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

    # process form data
	def post(self, request):
            form = self.form_class(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                # cleaned (normalized) data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()

                # returns User objects if credentials are correct
                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, 'main/index.html')

            return render(request, self.template_name, {'form': form})




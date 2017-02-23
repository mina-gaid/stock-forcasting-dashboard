from django.shortcuts import render

def index(request):
	return render(request, 'main/index.html')
	
def about(request):
	return render(request, 'main/about.html')

def support(request):
	return render(request, 'main/faq.html')
	
def contact(request):
	return render(request, 'main/contact.html')
	
def terms(request):
	return render(request, 'main/terms-and-conditions.html')

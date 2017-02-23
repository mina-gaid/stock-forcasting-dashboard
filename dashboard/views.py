from django.shortcuts import render

def panel(request):
	return render(request, 'dashboard/control-panel.html')

def tables(request):
	return render(request, 'dashboard/tables.html')

def charts(request):
	return render(request, 'dashboard/charts.html')

from django.shortcuts import render


def scale(request):
	return render(request, 'fake/scale.html', {})

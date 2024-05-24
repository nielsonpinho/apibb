from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout

def logout_view(request):
    """Faz um logout no usuario"""
    logout(request)
    
    return HttpResponseRedirect(reverse('login'))


# Create your views here.

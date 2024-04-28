
from .models import ServiceRequest


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ServiceRequestForm
from .models import Customer
from django.contrib.auth import authenticate, login






@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request=request,data=request.POST)
        if form.is_valid():
            customer = Customer.objects.get(user=request.user)
            service_request = form.save(commit=False)
            service_request.customer = customer
            service_request.save()
            return redirect('request_status')  # Redirect to request_status view
    else:
        form = ServiceRequestForm()
    return render(request, 'submit_request.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('submit_request')  # Redirect to submit_request view
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

@login_required
def request_status(request):
    try:
        customer = Customer.objects.get(user=request.user)
        service_requests = ServiceRequest.objects.filter(customer=customer)
        return render(request, 'request_status.html', {'service_requests': service_requests})
    except Customer.DoesNotExist:
        # Handle case where customer profile does not exist
        return render(request, 'request_status.html', {'service_requests': []})

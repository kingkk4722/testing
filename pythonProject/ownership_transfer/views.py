# ownership_transfer/views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import RegistrationForm
from .models import Ownership,UserProfile
from django.contrib import messages
from .forms import OwnershipForm,OwnershipTransferForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests
import random
from sinch import Client

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect('account_home')
    else:
        form = RegistrationForm()
    return render(request, 'ownership_transfer/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account_home')
    else:
        form = AuthenticationForm()
    return render(request, 'ownership_transfer/login.html', {'form': form})

@login_required(login_url='login')
def account_home(request):
    # Fetch user profile associated with the current user
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Fetch ownerships for the current user
    user_ownerships = Ownership.objects.filter(owner=request.user).values('id','model','owner','IMEI_Number')

    # Create an instance of the OwnershipForm
    form = OwnershipForm()

    # Pass user profile, ownerships, and form to the context
    context = {
        'user_profile': user_profile,
        'user_ownerships': user_ownerships,
        'form': form,
    }

    # Render the template with the provided context
    return render(request, 'ownership_transfer/account_home.html', context)

@login_required(login_url='login')
def transfer_ownership(request, ownership_id):
    ownership = get_object_or_404(Ownership, id=ownership_id)

    # Check if the current user is the owner of the ownership
    if request.user != ownership.owner:
        messages.error(request, "You do not have permission to transfer ownership of this device.")
        return redirect('account_home')  # or any other appropriate redirect

    if request.method == 'POST':
        # Use the OwnershipTransferForm in the POST request handling logic
        form = OwnershipTransferForm(request.POST)
        if form.is_valid():
            # Assuming you have a form or something to get the new owner
            new_owner_username = form.cleaned_data['new_owner_username']  # Adjust this based on your actual form field
            new_owner = get_object_or_404(User, username=new_owner_username)

            # Update the owner of the ownership
            ownership.owner = new_owner
            ownership.save()

            messages.success(request, "Ownership transferred successfully.")
            return redirect('account_home')  # or any other appropriate redirect
    else:
        # Create an instance of the OwnershipTransferForm for the initial rendering
        form = OwnershipTransferForm()

    # Render the page with the form to transfer ownership
    return render(request, 'ownership_transfer/transfer_ownership.html', {'ownership': ownership, 'form': form})


def home(request):
    if request.method == 'POST':
        imei_number = request.POST.get('IMEI_Number')
        try:
            ownership = Ownership.objects.get(IMEI_Number=imei_number)
        except Ownership.DoesNotExist:
            # Handle the case where no matching Ownership object is found
            error_message = f"Device with IMEI {imei_number} not found."
            return render(request, 'ownership_transfer/home.html', {'error_message': error_message})
        else:
            return render(request, 'ownership_transfer/device_info.html', {'ownership': ownership})
    else:
        return render(request, 'ownership_transfer/home.html')
def logout_view(request):
    logout(request)
    # Additional logic or redirect if needed
    return redirect('home')

def add_smartphone(request):
    if request.method == 'POST':
        model = request.POST.get('model')
        owner = request.user
        IMEI_Number = request.POST.get('IMEI_Number')
        Ownership.objects.create(model=model, owner=owner, IMEI_Number=IMEI_Number)
        messages.success(request, "New Device added.")
        return redirect('account_home')
    else:
        messages.error(request, "Something went wrong!!.")
    return redirect('account_home')


def add_smartphone_page(request):
    return render(request,'ownership_transfer/add_smartphone.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, AccountEditForm
from .models import UserExtraInfo
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    return HttpResponse(render(request, 'account/signup.html', {'form': form}))


@login_required
def account_page(request):
    try:
        user_extra_info = request.user.userextrainfo
    except ObjectDoesNotExist:
        user_extra_info = UserExtraInfo(user=request.user)
        user_extra_info.save()

    form = AccountEditForm(request.POST or None, instance=user_extra_info)

    if form.is_valid() and request.POST:
        extra_user_info = form.save(commit=False)
        extra_user_info.user = request.user
        extra_user_info.profile_picture = request.FILES['profile_picture']
        extra_user_info.save()
        return redirect('/account')

    return HttpResponse(render(request, 'account/account_page.html', {'form': form}))


# @login_required
# def account_edit_page(request):
#
#     form = AccountEditForm(request.POST or None, instance=request.user.userextrainfo)
#
#     if form.is_valid() and request.POST:
#         extraUserInfo = form.save(commit=False)
#         extraUserInfo.user = request.user
#         extraUserInfo.save()
#         return redirect('/account')
#
#     return HttpResponse(render(request, 'account/account_edit_page.html', {'form': form}))

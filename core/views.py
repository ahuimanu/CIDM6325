# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # optional: give them basic permissions or group here
            login(request, user)  # log them in right away
            return redirect("blog:post_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


class GetLogoutView(View):
    """Allow GET /accounts/logout/ so Melodi can log out from the header."""
    def get(self, request, *args, **kwargs):
        logout(request)
        # same place we send users everywhere else
        return redirect("blog:post_list")

    def post(self, request, *args, **kwargs):
        # still support POST
        logout(request)
        return redirect("blog:post_list")

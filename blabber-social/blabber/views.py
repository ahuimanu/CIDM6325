from django.shortcuts import render
from .models import Profile


# Create your views here.
def dashboard(request):
    return render(request, "blabber/dashboard.html")


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "blabber/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    # if a profiles was not previously created
    if not hasattr(request.user, "profile"):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)

    # check to see if follow/unfollow buttons were pressed
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    return render(request, "blabber/profile.html", {"profile": profile})

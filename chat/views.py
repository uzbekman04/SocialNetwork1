from django.shortcuts import render
from . import models
from accounts.models import Profile
from .forms import MessageForm


# Create your views here.
def ChatView(request):
    profiles = Profile.objects.all()
    profs = []
    for profile in profiles:
        if ((profile in models.Message.sender and request.user in models.Message.receiver) or
                (profile in models.Message.receiver and request.user in models.Message.sender)):
            profs.append(profile)
    return render(request, 'chat_dashboard.html', context={'profiles': profs})


def ChattingView(request, pk):
    sender = Profile.objects.get(user=request.user)
    receiver = Profile.objects.get(pk=pk)
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(request.POST)
        message = form.save()
        message.sender = sender
        message.receiver = receiver
        message.save()
    messages = models.Message.objects.filter(sender=sender, receiver=receiver)
    return render(request, 'chat.html', context={'form': form, "messages": messages})
from django.shortcuts import render
from .models import Device, Command, Event
from .forms import DeviceForm, CommandForm, EventForm, EventTriggerForm

from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from NeoGPIO.IRLearner import IRLearner
from NeoGPIO.IRSender import IRSender
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

from datetime import datetime
import time

scheduler = BackgroundScheduler()
scheduler.start()

def welcome(request):
    """ Display welcome text """
    if not request.user.is_authenticated():
        return render(request, 'willy/index.html', {})
    return redirect('device_list')

def guess_protocol(device_name):
    """ Guess device protocol from its name """
    for name in ["sony", "samsung", "epson"]:
        if name in device_name.lower():
            return name
    return ""

def send_command_once(event):
    """ Send a command once """
    try:
        to_send = Event.objects.get(pk=event.pk)
        IRSender().send(to_send.command.code, guess_protocol(to_send.device.name))
        to_send.delete()
    except Event.DoesNotExist:
        pass

@login_required
def device_list(request):
    """ Display the user's device list"""
    devices = Device.objects.filter(author=request.user).order_by('name')
    return render(request, 'willy/device_list.html', {'devices': devices})

@login_required
def device_new(request):
    """ Form logic for registering a new device """
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.author = request.user
            device.save()
            return redirect('device_detail', pk=device.pk)
    else:
        form = DeviceForm()
    return render(request, 'willy/device_edit.html', {'form': form})

@login_required
def add_command_to_device(request, pk):
    """ Form logic for learning a new command for a device """
    device = get_object_or_404(Device, pk=pk)
    if request.method == "POST":
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.save(commit=False)
            command.device = device
            learner = IRLearner()
            code = learner.getCode(guess_protocol(device.name))
            if code:
                command.code = code
                command.save()
                return redirect('device_detail', pk=device.pk)
            messages.error(request, 'No command received!')
            return render(request, 'willy/add_command_to_device.html', {'form': form})
    else:
        form = CommandForm()
    return render(request, 'willy/add_command_to_device.html', {'form': form})

@login_required
def schedule_command(request, pk):
    """ Form logic for scheduling a command """
    commands = get_list_or_404(Command, device=pk)
    device = get_object_or_404(Device, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # if event.scheduled_time < datetime.now():
            #     messages.error(request, 'Scheduled time needs to be in the future!')
            #     return render(request, 'willy/schedule_command.html', {'form': form, 'device': device})

            event.device = device
            event.save()

            # scheduler logic for just-once / daily events
            if event.everyday:
                event_time = event.scheduled_time
                scheduler.add_job(lambda: IRSender().send(event.command.code, guess_protocol(device.name)), 'cron', hour=event_time.hour, minute=event_time.minute, id=str(event.pk))
            else:
                scheduler.add_job(lambda: send_command_once(event), 'date', run_date=event.scheduled_time, id=str(event.pk))
            return redirect('device_detail', pk=device.pk)
    else:
        form = EventForm()

        # only display commands that belong to this device
        form.fields["command"].queryset = Command.objects.filter(device=device.pk)
    return render(request, 'willy/schedule_command.html', {'form': form, 'device': device})

@login_required
def event_remove(request, pk):
    """ Remove and event from the scheduler queue """
    event = get_object_or_404(Event, pk=pk)
    try:
        scheduler.remove_job(str(event.pk))
    except JobLookupError:
        pass
    device = event.device
    event.delete()
    return redirect('device_detail', pk=device.pk)

@login_required
def trigger_command(request, pk):
    """ Trigger a command """
    commands = get_list_or_404(Command, device=pk)
    device = get_object_or_404(Device, pk=pk)
    if request.method == "POST":
        form = EventTriggerForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.device = device
            IRSender().send(event.command.code, guess_protocol(device.name))
            return redirect('device_detail', pk=device.pk)
    else:
        form = EventTriggerForm()

        # only display commands that belong to this device
        form.fields["command"].queryset = Command.objects.filter(device=device.pk)
    return render(request, 'willy/trigger_command.html', {'form': form, 'device': device})

@login_required
def trigger_one_command(request, device_pk, command_pk):
    """ Trigger a specific command """
    command = get_object_or_404(Command, pk=command_pk)
    device = get_object_or_404(Device, pk=device_pk, author=request.user)
    IRSender().send(command.code, guess_protocol(device.name))
    return render(request, 'willy/device_detail.html', {'device': device})

@login_required
def device_detail(request, pk):
    """ Display a device's details """
    device = get_object_or_404(Device, pk=pk, author=request.user)
    return render(request, 'willy/device_detail.html', {'device': device})

@login_required
def device_edit(request, pk):
    """ Edit device name """
    device = get_object_or_404(Device, pk=pk, author=request.user)
    if request.method == "POST":
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device = form.save(commit=False)
            device.author = request.user
            device.save()
            return redirect('device_detail', pk=device.pk)
    else:
        form = DeviceForm(instance=device)
    return render(request, 'willy/device_edit.html', {'form': form})

@login_required
def device_remove(request, pk):
    """ Remove a device """
    device = get_object_or_404(Device, pk=pk, author=request.user)
    device.delete()
    return redirect('device_list')

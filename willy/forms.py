from django import forms

from .models import Device, Command, Event

from datetimewidget.widgets import DateTimeWidget

class DeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ('name',)

class CommandForm(forms.ModelForm):

    class Meta:
        model = Command
        fields = ('name',)

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('scheduled_time', 'command', 'everyday')
        dateTimeOptions = {
            'format': 'dd/mm/yyyy HH:ii P',
            'autoclose': True,
            'showMeridian' : True
        }
        widgets = {
            'scheduled_time': DateTimeWidget(attrs={'id':"yourdatetimeid"},
                                             usel10n=True,
                                             bootstrap_version=3,
                                             options=dateTimeOptions),
        }

class EventTriggerForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('command',)
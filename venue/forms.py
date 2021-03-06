from django.forms import ModelForm, ValidationError
from django.forms import DateTimeInput, CharField, PasswordInput
from .models import Booking
from django.contrib.auth.forms import AuthenticationForm
from attendance.models import Batch
from .models import EventCalander
import json
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
class VenueBookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time','end_time','venue','title','description','notification_email']
        labels = {
            "title":"Purpose of booking",
            "description":"More details about the event"
        }
    def clean(self):
        cleaned_data = super(VenueBookingForm, self).clean()
        venue = cleaned_data.get('venue')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        venue = cleaned_data.get('venue')
        if start_time > end_time:
            #print(start_time)
            raise ValidationError("The start time is after the end time")
        # Check all calandars in database and eventCal for the venue and time
        batches = Batch.objects.filter(active=True)
        eventcals = EventCalander.objects.filter(active=True)
        calids = []
        for batch in batches:
            calids.append(batch.calander_id)
        for eventcal in eventcals:
            calids.append(eventcal.calander_id)
        scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'account.json', scopes,
        )
        http = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http=http)
        for cal in calids:
            events = service.events().list(
                calendarId=cal,
                singleEvents=True,
                timeMin=start_time.strftime("%Y-%m-%dT%H:%M:%S.%f+05:30"),
                timeMax=end_time.strftime("%Y-%m-%dT%H:%M:%S.%f+05:30"),
                ).execute()["items"]
            print(events)
            if len(events) > 0:
                for event in events:
                    if event.get("location") == venue.name:
                        raise ValidationError("{} is not available at requested time slot because of clash with {}".format(venue.name,event["summary"]))
        return cleaned_data

class CaptchaForm(VenueBookingForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta(VenueBookingForm.Meta):
        fields = VenueBookingForm.Meta.fields + ['captcha']

class StatusForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['status']
class LoginForm(AuthenticationForm):
    username = CharField(max_length=30)
    password = CharField(max_length=30, 
                               widget=PasswordInput(attrs={'name': 'password'}))
from django.shortcuts import render, redirect
from django.views import generic
from .models import Booking
from .forms import VenueBookingForm, StatusForm, CaptchaForm
from django.contrib.auth.decorators import permission_required
from attendance.tasks import send_email
from django.shortcuts import reverse
from .tasks import insert_event
from attendance.models import Batch
from  .models import EventCalander
# Create your views here.
from attendance.forms import ConfirmForm

class BookEvent(generic.edit.CreateView):
    success_url = 'thankyou'
    form_class = CaptchaForm
    template_name = 'venue/booking_form.html'

class Thankyou(generic.TemplateView):
    template_name = 'venue/thankyou.html'

class EventList(generic.ListView):
    model = Booking
    context_object_name = 'bookings'
    template_name = 'venue/list.html'
    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['approved'] = Booking.objects.filter(status='3').order_by('-start_time')
        context['denied'] = Booking.objects.filter(status='2').order_by('-start_time')
        context['awaiting'] = Booking.objects.filter(status='1').order_by('-start_time')
        return context

class EventDetail(generic.UpdateView):
    model = Booking
    fields = ['status']
    template_name = 'venue/detail.html'
    success_url = '/venue/list'
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(EventDetail, self).dispatch(
            request, *args, **kwargs)

@permission_required('attendance.preclaim_dean_approve')
def approve_booking(request, pk):
    if request.method == 'GET':
        booking = Booking.objects.get(pk=int(pk))
        
        # create google calander event
        print(type(booking.start_time))
        start = booking.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f+05:30")
        end = booking.end_time.strftime("%Y-%m-%dT%H:%M:%S.%f+05:30")
        insert_event.delay(
            booking.title,
            booking.venue.name,
            booking.description,
            start,
            end,
            )
        
        booking.status='3'
        booking.save()

        #send email to notify
        send_email.delay("Venue Booking Approved", "The Booking for {}  at {} has been approved.".format(booking.title,booking.venue.name),'venue@mail.manipalconnect.com',[booking.notification_email])
        return render(request,'venue/approved.html',{'booking':booking})

@permission_required('attendance.preclaim_dean_approve')
def delete_booking(request,pk):
    booking = Booking.objects.get(pk=int(pk))
    if request.method == 'GET':
        return render(request,'venue/confirm.html',{'booking':booking,'form':ConfirmForm})
    
    if request.method == 'POST':
        f = ConfirmForm(request.POST)
        if f.is_valid():
            reason = f.cleaned_data.get('reason')
        booking.delete()
        send_email.delay("Booking for {} Rejected".format(booking.title), "Reason: {}".format(reason), 'venue@mail.manipalconnect.com', [booking.notification_email])
        return render(request,'venue/dissapproved.html',{'reason':reason,'booking':booking})

def download_calanders(request):
    batches = Batch.objects.filter(active=True)
    eventcals = EventCalander.objects.filter(active=True)
    return render(request,'calander_download.html',{'batches':batches,'eventcals':eventcals})

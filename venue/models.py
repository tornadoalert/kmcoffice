from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from sesame import utils
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.template.loader import render_to_string
from attendance.tasks import send_email
from .quotes import get_random_quote
# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Booking(models.Model):
    APPROVAL_CHOICES = (
    (u'2', u'No'),
    (u'3', u'Yes'),
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.ForeignKey(Venue,models.CASCADE,'bookings')
    status = models.CharField(max_length=1,default='1',choices=APPROVAL_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    notification_email = models.EmailField(default='')

    def __str__(self):
        return self.title

    def multiday(self):
        if self.start_time.day == self.end_time.day:
            return False
        else:
            return True

def add_auth_token(link,login_token):
    link+='?method=magic&url_auth_token={}'.format(login_token['url_auth_token'])
    return link

@receiver(post_save, sender=Booking)
def create_booking(sender, instance, created, **kwargs):
    if created:
        #users = [user for user in User.objects.all() if user.has_perm('attendance.preclaim_dean_approve')]
        user = User.objects.get(username='dean')
        #print("Found {} user with dean permission".format(len(users)))
        
        login_token = utils.get_parameters(user)
        #print()
        approve_link = reverse('approve_booking',kwargs={'pk':instance.pk})
        approve_link = add_auth_token(approve_link,login_token)
        #print(approve_link)
        disapprove_link = reverse('disapprove_booking',kwargs={'pk':instance.pk})
        disapprove_link = add_auth_token(disapprove_link,login_token)
        #print(disapprove_link)
        url = 'http://kmcmanipal.herokuapp.com'
        approve_link = url+approve_link
        disapprove_link = url+disapprove_link
        body = render_to_string(
            'venue/email/dean.html',{
                'approve':approve_link,
                'disapprove':disapprove_link,
                'booking':instance,
                'quote':get_random_quote()})
        #print(user.email)
        send_email.delay("Venue Booking Approval",'',from_email='venue@mail.manipalconnect.com',recipient_list=[user.email], html_message=body)
class EventCalander(models.Model):
    name = models.CharField(max_length=200, default='Default Event')
    calander_id = models.TextField()
    active = models.BooleanField(default=True)

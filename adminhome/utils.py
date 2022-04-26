import datetime, pytz

from .models import  Booking

def isPreviousBooking(booking_obj):
   return booking_obj.end_time.replace(tzinfo=pytz.utc) < datetime.datetime.now(pytz.timezone('US/Central'))

def isCurrentBooking(booking_obj):
   return booking_obj.start_time.replace(tzinfo=pytz.utc) <= datetime.datetime.now(pytz.timezone('US/Central')) and booking_obj.end_time.replace(tzinfo=pytz.utc) >= datetime.datetime.now(pytz.timezone('US/Central'))


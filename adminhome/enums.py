from email.policy import default
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class BookingStates(models.TextChoices):
    NEW = 'new', _('New Booking')
    PENDING_APPROVAL = 'pending_approval', _('Pending Approval')
    PENDING_LEASE = 'pending_lease', _('Pending Lease')
    PENDING_SLOT = 'pending_slot', _('Pending Slot')
    REJECTED = 'rejected', _('Rejected Booking')
    APPROVED = 'approved', _('Approved Booking')
    CANCELED_BEFORE_LEASE = 'canceled_before_lease', _('Canceled Before Lease')
    CANCELED = 'canceled', _('Canceled Booking')
    PAID = 'paid', _('Paid Booking')
    # UNPAID = 'unpaid', _('Unpaid Booking')

class PaymentStatus(models.TextChoices):
    PAID = 'paid', _('Paid')
    UNPAID = 'unpaid', _('Unpaid')

class PaymentMethod(models.TextChoices):
    CASH = 'cash', _('Cash Payment')
    CARD = 'card', _('Card Payment')
    ONLINE = 'online', _('Online Payment')

class ViewBookings(models.TextChoices):
    UPCOMING_BOOKINGS = 'upcoming_bookings', _('Upcoming Bookings')
    PREVIOUS_BOOKINGS = 'previous_bookings', _('Previous Bookings')
    CURRENT_BOOKINGS = 'current_bookings', _('Current Bookings')
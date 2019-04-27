from django.db import models
from django.contrib.auth.models import User, Group

class PhoneNumberManager(models.Manager):
    def get_reply_numbers(self, pn_user):
        pn_number = pn_user.number
        muted_by = pn_user.muted_by.all()
        return [pn.number for pn in self.exclude(number=pn_number).exclude(
            owner__in=muted_by).exclude(is_active=False)]

class PhoneNumber(models.Model):
    """Phone numbers for the smack texting."""
    number = models.CharField(max_length=10)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    muted_by = models.ManyToManyField(User, related_name="muted_users")
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=True)
    is_operator = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s, for %s' % (self.number, self.owner.username)

    objects = PhoneNumberManager()

class Message(models.Model):
    text = models.CharField(max_length=2048)
    sid = models.CharField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"<Message: %s>" % (self.sid)

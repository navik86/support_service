from django.db import models
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.CASCADE, verbose_name='parent',
                               related_name='replys')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.user.name} on {self.ticket}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Ticket(models.Model):
    TICKET_STATUS = [
        (0, 'In waiting'),
        (1, 'In works'),
        (2, 'Done'),
    ]
    status = models.SmallIntegerField(choices=TICKET_STATUS, default=0)
    client = models.ForeignKey(User, on_delete=models.CASCADE,
                               limit_choices_to={'support': False}, related_name='client')
    support_ticket = models.ForeignKey(User, on_delete=models.CASCADE,
                                       limit_choices_to={'support': True}, related_name='supports')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    star_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']

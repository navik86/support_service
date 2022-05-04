from django.contrib import admin

from tickets.models import Messages, Tickets


class TicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'client', 'support_ticket', 'created_at')
    list_display_links = ('id', 'title')
    save_on_top = True


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'user', 'created_at', 'parent')
    list_display_links = ('id', 'ticket')
    list_filter = ('user',)
    save_on_top = True


admin.site.register(Tickets, TicketsAdmin)
admin.site.register(Messages, MessagesAdmin)

admin.site.site_header = 'Управление заявками'

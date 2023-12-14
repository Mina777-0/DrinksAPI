from django.contrib import admin
from .models import MyUser, Drink

class MemberAdmin(admin.ModelAdmin):
    list_display= ("title", "price")
    prepopulated_fields= {"slug": ("title", "price")}


admin.site.register(MyUser)
admin.site.register(Drink, MemberAdmin)
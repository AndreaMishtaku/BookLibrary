from django.contrib import admin
from .models import Book,MyUser,Contact,Rating,Order
from django.contrib.auth.models import Group

# Register your models here.
admin.site.unregister(Group)

@admin.register(MyUser)
class userAdmin(admin.ModelAdmin):
    list_display=('id','firstname','lastname','email','phone','age','city')

    def has_add_permission(self, request):
        return False


@admin.register(Book)
class bookAdmin(admin.ModelAdmin):
    list_display=('ISBN','book_title','book_author','publisher','year_of_publication')


@admin.register(Contact)
class contactAdmin(admin.ModelAdmin):
    list_display=('email','message','date_sended')

    def has_add_permission(self, request):
        return False


@admin.register(Rating)
class ratingAdmin(admin.ModelAdmin):
    list_display=('user_id','book_isbn','rating')

    def has_add_permission(self, request):
        return False

@admin.register(Order)
class orederAdmin(admin.ModelAdmin):
    list_display=('user_id','book_isbn','date_s','date_e','confirmed')


    def has_add_permission(self, request):
        return False


    actions=['confirm_order']
    @admin.action(description='Confirm order')
    def confirm_order(self, request, queryset):
        queryset.update(confirmed=True)

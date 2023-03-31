from django.contrib import admin
from .models import Author, Book, Genre, Status, Language, BookInstance

#anton Dbnt,cr1
# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Status)
admin.site.register(Language)
admin.site.register(BookInstance)


# @admin.register(BookInstance)
# class BookInstanceAdmin(admin.ModelAdmin):
#     list_display = ('book', 'status', 'borrower', 'due_back', 'id')
#     list_filter = ('status', 'due_back')
    
#     fieldsets = (
#         (None, {
#             'fields': ('book', 'imprint', 'inv_nom')
#             }),
#         ('Availability', {
#            'fields': ('status', 'due_back', 'borrower') 
#         }),
#     )
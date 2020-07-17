from django.contrib import admin

# Register your models here
from main.models import Question, Answere
admin.site.register((Question, Answere))

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


models = apps.get_models()
try:
    for model in models:
        admin.site.register(model)
except AlreadyRegistered:
    print("Все модели добавлены в админку")

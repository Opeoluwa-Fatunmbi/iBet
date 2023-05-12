from django.contrib import admin
from django.apps import apps

# loop through all the models in .models and admin.site .register it
for model in apps.get_models():
    if model._meta.app_label == 'api' and model._meta.model_name != 'group':
        admin.site.register(model)

from django.contrib import admin

from django.contrib.admin import ModelAdmin

from log.models import Log, Motion, Video


@admin.register(Motion)
class MotionAdmin(ModelAdmin):
    list_display = ['id', 'name', 'index']


@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = ['motion', 'name']


@admin.register(Log)
class LogAdmin(ModelAdmin):
    list_display = ['user', 'motion', 'count', 'created_at']

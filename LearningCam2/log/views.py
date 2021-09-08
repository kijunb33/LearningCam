import random
import json
import zipfile
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView

from log.models import Motion, Log, Video


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'log/index.html'


class SummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'log/summary.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()

        daily_data = []
        for motion in Motion.objects.all():
            log = Log.objects.filter(user=self.request.user,
                                     motion=motion,
                                     created_at=now()).first()

            daily_data.append(log.count if log else 0)

        if sum(daily_data) != 0:
            context_data['daily_data'] = list(map(lambda x: x / sum(daily_data) * 100, daily_data))
        else:
            context_data['daily_data'] = daily_data

        weekly_data = []
        recommend_data = {}
        for motion in Motion.objects.all():
            weekly_day_data = []
            x_data = []
            for i in range(7):
                date = now() - timedelta(days=(6 - i))
                x_data.append(date.strftime('%Y-%m-%d'))
                log = Log.objects.filter(user=self.request.user,
                                         motion=motion,
                                         created_at=date).order_by('created_at').first()
                weekly_day_data.append(log.count if log else 0)
            recommend_data[motion] = sum(weekly_day_data)
            weekly_data.append(weekly_day_data)
        for i in range(7):
            sum_of_daily = sum(map(lambda x: x[i], weekly_data))
            if sum_of_daily != 0:
                for weekly_day_data in weekly_data:
                    weekly_day_data[i] /= sum_of_daily * 100

        context_data['weekly_data'] = weekly_data
        context_data['x_data'] = x_data

        motion = max(recommend_data.keys(), key=(lambda key: recommend_data[key]))
        if motion.name != '정자세':
            context_data['bad_motion'] = motion
            context_data['recommend'] = random.choice(Video.objects.filter(motion=motion).all())

        return context_data


class VideoView(LoginRequiredMixin, ListView):
    template_name = 'log/video.html'
    context_object_name = 'motion_list'
    model = Motion


class VideoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'log/video_detail.html'
    context_object_name = 'video'
    model = Video

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()

        video = self.object
        img_urls = list()
        if video.img1:
            img_urls.append('/' + video.img1.name)
        if video.img2:
            img_urls.append('/' + video.img2.name)
        if video.img3:
            img_urls.append('/' + video.img3.name)

        context_data['img_urls'] = img_urls
        return context_data


class VideoDetailModelView(LoginRequiredMixin, DetailView):
    context_object_name = 'video'
    model = Video

    def get(self, request, *args, **kwargs):
        video = self.get_object()
        if not video.model:
            return HttpResponse()
        zf = zipfile.ZipFile(video.model.file.file, 'r')
        filename = self.kwargs['filename']
        if filename not in zf.namelist():
            return HttpResponse()
        return HttpResponse(zf.read(filename))


@method_decorator(csrf_exempt, name='dispatch')
class AddLogView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        for i in range(len(data)):
            if data[i] == 0:
                continue
            motion = Motion.objects.get(index=i)
            log = Log.objects.filter(user=request.user,
                                     motion=motion,
                                     created_at=now()).first()
            if log is None:
                log = Log(user=request.user,
                          motion=motion,
                          count=0)
            log.count += data[i]
            log.save()
        return HttpResponse("OK")

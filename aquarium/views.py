from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone
from phweb.models import Deg, Ph, Redox
from aquarium.charts import TodayChart, CurrentWeekChart, ArchiveChart, LastWeekChart, Last30DaysChart, YearChart
from .forms import DegreeChartForm

class IndexView(TemplateView):
    template_name = 'aquarium/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        if (not user is None) and user.is_authenticated():
            context['deg']   = Deg.objects.filter(user=user).last()
            context['ph']    = Ph.objects.filter(user=user).last()
            context['redox'] = Redox.objects.filter(user=user).last()
            try:
                context['todaychart'] = TodayChart(user)
            except Exception:
                context['todaychartNoData'] = "Sorry. No data are available."
            context['week_chart'] = CurrentWeekChart(user)
            context['last_week_chart'] = LastWeekChart(user)
            context['last_30days_chart'] = Last30DaysChart(user)
        return context


class YearView(TemplateView):
    template_name = 'aquarium/year.html'

    def get_context_data(self, **kwargs):
        context = super(YearView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            context['year_chart'] = YearChart(user)
        return context



def get_graph_year(request, year):
    if request.method == 'POST':
        form = DegreeChartForm(request.POST)
        if form.is_valid():
            start_date = form['start_date'].value()
            y, m, d = start_date.split("-")
            start_date = timezone.datetime(int(y), int(m), int(d))
            start_date = timezone.make_aware(start_date)
            end_date   = form['end_date'].value()
            y, m, d = end_date.split("-")
            end_date = timezone.datetime(int(y), int(m), int(d))
            end_date = timezone.make_aware(end_date)
            archive_chart = ArchiveChart(request.user, start_date, end_date)
            return render(request, 'aquarium/archive.html', {'achart' : archive_chart,
                                                             'form': form,
                                                             'year': year})
    else:
        form = DegreeChartForm(initial={'start_date': year + "-06-01", 'end_date': year + "-08-10"})
        return render(request, 'aquarium/archive.html', {'form': form, 'year': year})


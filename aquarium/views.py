from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone
from phweb.models import Deg, Ph, Redox, Piscine, Battery
from aquarium.charts import TodayChart, CurrentWeekChart, ArchiveChart, LastWeekChart, Last30DaysChart, YearChart
from .forms import DegreeChartForm


def check_user_has_pool(user):
    piscine_id_list = [piscine.user for piscine in Piscine.objects.all()]
    return user in piscine_id_list

class IndexView(TemplateView):
    template_name = 'aquarium/index.html'

    def ph_warning(self, ph):
        if ph:
            if ph.phval < 7.5:
                return (True, (7.5 - float(ph.phval)) )
            elif ph.phval > 8.2:
                return (True, (8.2 - float(ph.phval)) )
            else:
                return (False, 0)
        return (False, 0)

    def redox_warning(self, redox):
        if redox:
            difference = abs(650 - float(redox.redoxval))
            if difference > 200:
                return (True, difference)
            else:
                return (False, difference)
        return (False, 0)


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        if not check_user_has_pool(user):
            context['user_has_no_pool'] = user
            return context
        else:
            context['user_has_pool'] = user
        if (not user is None) and user.is_authenticated():
            context['deg']   = Deg.objects.filter(user=user).last()
            ph = Ph.objects.filter(user=user).last()
            context['ph']    = ph
            ph_warning_difference = self.ph_warning(ph)
            if ph_warning_difference[0]:
                context['ph_warning'] = ph_warning_difference[1]
            redox = Redox.objects.filter(user=user).last()
            warning_and_difference = self.redox_warning(redox=redox)
            context['redox'] = redox
            if warning_and_difference[0]:
                context['redox_warning'] = warning_and_difference[1]

            context['battery'] = Battery.objects.filter(user=user).last()
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


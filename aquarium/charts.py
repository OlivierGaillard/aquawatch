from jchart import Chart
from jchart.config import Axes, DataSet
from phweb.models import Deg, Ph, Redox
from datetime import timedelta
from django.utils import timezone
import logging


logname = 'server.log'
logging.basicConfig(format='%(levelname)s\t: %(asctime)s : %(message)s', filename=logname,
                    filemode='a', level=logging.DEBUG)



class ArchiveChart(Chart):

    def __init__(self, user, start_date, end_date):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date
        super(ArchiveChart, self).__init__()


    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }



    def _get_data_class(self, datatype):
        types = {'Deg': Deg, 'pH' : Ph, 'Redox' : Redox}
        data_class = types[datatype]
        return data_class

    def set_label(self, msg="", start_date_str="", end_date_str=''):
        return self.data_class.get_graph_name() + " du {0} au {1}".format(start_date_str, end_date_str),

    def get_datasets(self, datatype):
        self.data_class = self._get_data_class(datatype)
        user_data  = self.data_class.objects.all().filter(user=self.user)
        range_data  = user_data.filter(date__range = (self.start_date, self.end_date))
        dataset     = [{'y' : data.get_value(), 'x': data.date} for data in range_data]
        start_date_str = "{0}/{1}/{2}".format(self.start_date.day, self.start_date.month, self.start_date.year)
        end_date_str   = "{0}/{1}/{2}".format(self.end_date.day, self.end_date.month, self.end_date.year)
        return [DataSet(
            type = 'line',
            #label = data_class.get_graph_name() + " du {0} au {1}".format(start_date_str, end_date_str),
            label = self.set_label(start_date_str=start_date_str, end_date_str=end_date_str),
            data = dataset,
            #backgroundColor = 'rgb(63, 136, 191)',
        ), ]

    def get_first_day_of_week(date):
        "Utility method"
        week_day = date.isoweekday()
        return date - timedelta(days=week_day - 1)

    def get_today_date(self):
        t0 = timezone.localtime()
        today_midnight = timezone.datetime(year=t0.year, month=t0.month, day=t0.day)
        today_midnight = timezone.make_aware(today_midnight)
        return today_midnight.date()


    def exists_today_data(self):
        logging.debug("In exists_today_data for user: %s", self.user.username)
        d = Deg.objects.filter(user=self.user).last()
        if d:
            logging.debug("Last degree: %s", d)
            return timezone.localtime().date() == d.date.date()
        else:
            logging.debug("No last data found")
            return False

    def get_end_day(self):
        """Get the last hour of data: today or in the past."""
        if self.exists_today_data():  # today and last data day are equal
            logging.debug("In get_end_day, after called exists_today_data: today data exists")
            return timezone.localtime()
        else:
            logging.debug("In get_end_day, after called exists_today_data: today data does not exist")
            d = Deg.objects.filter(user=self.user).last()
            return d.date  # last hour of data


class TodayChart(ArchiveChart):

    def __init__(self, user):
        logging.info("Init of TodayChart for user: %s", user.username)
        self.user = user
        d = Deg.objects.last()
        self.start_date = None
        self.end_date = self.get_end_day()
        if self.exists_today_data(): # TODO: test it
            self.start_date = self.get_today_date()  # today midnight
        else:
            # start = midnight of last day with data
            self.start_date = timezone.datetime(year=d.date.year, month=d.date.month, day=d.date.day)
            self.start_date = timezone.make_aware(self.start_date)
            #self.end_date = d.date # last hour of data
        super(TodayChart, self).__init__(self.user, self.start_date, self.end_date)

    def set_label(self, msg="", start_date_str="", end_date_str=""):
        return self.data_class.get_graph_name() + " des dernières heures."



class CurrentWeekChart(ArchiveChart):
    """Return the data of the current week."""

    def __init__(self, user):
        self.user = user
        self.end_date = self.get_end_day()
        #t0 = ArchiveChart.get_first_day_of_week(timezone.localtime())
        t0 = ArchiveChart.get_first_day_of_week(self.end_date)
        t0 = timezone.datetime(year=t0.year, month=t0.month, day=t0.day)  # exactly 00:00 hour
        t0 = timezone.make_aware(t0)
        self.start_date = t0
        #self.end_date = timezone.localtime()
        super(CurrentWeekChart, self).__init__(self.user, self.start_date, self.end_date)


class LastWeekChart(ArchiveChart):
    """Return the data of the previous week (not the current one."""

    def __init__(self, user):
        self.user = user
        last_week_day = timezone.localtime() + timedelta(days=-7)
        t0 = ArchiveChart.get_first_day_of_week(last_week_day)
        self.start_date = t0
        self.end_date = t0 + timedelta(days=6)
        super(LastWeekChart, self).__init__(self.user, self.start_date, self.end_date)


class Last30DaysChart(ArchiveChart):
    """Return the data of the previous week (not the current one."""

    def __init__(self, user):
        self.user = user
        t0 = timezone.localtime() + timedelta(days=-30)
        self.start_date = t0
        self.end_date = t0 + timedelta(days=30)
        super(Last30DaysChart, self).__init__(self.user, self.start_date, self.end_date)


class YearChart(ArchiveChart):

    def __init__(self, user):
        self.user = user
        t0 = timezone.datetime(year=2016, month=5, day=1)
        t0 = timezone.make_aware(t0)
        self.start_date = t0
        self.end_date = timezone.datetime(year=2016, month=11, day=1)
        self.end_date = timezone.make_aware(self.end_date)
        super(YearChart, self).__init__(self.user, self.start_date, self.end_date)


from django.test import LiveServerTestCase, Client, TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission
from datetime import timedelta
import random
from decimal import Decimal
from phweb.models import Deg
from .charts import Chart, TodayChart, CurrentWeekChart, ArchiveChart, LastWeekChart
from django.utils import timezone

class AquariumTest(LiveServerTestCase):
    """Cette classe sert à tester la visualisation des données:
    - obtention des dernières mesures
    - génération des graphiques.

    Cette classe sert aussi à tester les requêtes à construire pour les
    graphiques.
    """

    # Those fixtures load data from 2016
    #fixtures = ['DegNew.json'] #, 'PhNew.json', 'RedoxNew.json'] #, 'Ph.json', 'Redox.json']

    def get_random_degree(self):
        deg_value = random.randint(3, 30)
        deg_value += random.random()
        return deg_value


    def setUp(self):

        self.grone_user = User.objects.create_user(username="grone", password="raspigrone",
                                                   email="info@aquawatch.ch")
        self.user_boss_passwd = 'titi_grognon234'
        self.user_boss = 'Boss'
        self.boss = User.objects.create_user(username=self.user_boss, password=self.user_boss_passwd,
                                             email='info@metacoherence.ch')


        Deg.objects.all().update(user=self.boss)
        #deg = Deg.objects.first()

        deg_content_type = ContentType.objects.get_for_model(Deg)
        self.add_deg_perm = Permission.objects.get(codename='add_deg', content_type=deg_content_type, )
        self.del_deg_perm = Permission.objects.get(codename='delete_deg', content_type=deg_content_type)
        #
        self.user_boss2 = 'Boss2'
        self.user_boss2_passwd = 'toto_grognon344'
        self.boss2 = User.objects.create_user(username=self.user_boss2, password=self.user_boss2_passwd,
                                              email='info@metablue.ch')

        self.boss.user_permissions.add(self.add_deg_perm, self.del_deg_perm)
        self.boss2.user_permissions.add(self.add_deg_perm, self.del_deg_perm)

        # past_date = timezone.now() - timedelta(days=30)
        # self.deg = Deg.objects.create(celsius=19.00, user=self.boss, date=past_date)

    def tearDown(self):
        pass
        #self.deg.delete()

    def test_usergrone(self):
        self.assertIsNotNone(self.grone_user)

    def _extract_values(self, dataset):
        #print(dataset, len(dataset))
        mesure = dataset[0]
        #print('dataset[0]', mesure)
        values = mesure['data']
        return values


    def test_get_index_url(self):
        c = Client()
        response = c.get(self.live_server_url + '/')
        self.assertEqual(200, response.status_code)

    def test_chart_create_timeseries(self):
        chart = TodayChart(self.grone_user)
        self.assertIsNotNone(chart, 'chart was not created.')

    def test_chart_getdataset_for_user_startdate_today_interval_today_nodata(self):
        """ Uses the last values if no data are available today or for the week.
        """
        # Precondition:
        last_deg = Deg.objects.last()
        print(last_deg)
        chart = TodayChart(self.grone_user)
        # par défaut le graphe utilise la date du jour et affiche les valeurs du jour
        dataset = chart.get_datasets(datatype='Deg')
        self.assertIsNotNone(dataset)
        values = self._extract_values(dataset)
        self.assertTrue(len(values) > 0)


    def test_ArchiveChart_for_today(self):
        t0 = timezone.localtime()
        self.assertTrue(timezone.is_aware(t0))
        t1 = timezone.datetime(year=t0.year, month=t0.month, day=t0.day)  # exactly 00:00 hour
        t1 = timezone.make_aware(t1)
        # The date saved will be 22:00 UTC+0 but 00:00 UTC+2
        d1 = Deg.objects.create(celsius=8.0, user=self.boss, date=t0)
        self.assertEqual(d1.date, t0)
        d2 = Deg.objects.create(celsius=8.5, user=self.boss, date=t1)

        for d in Deg.objects.all():
            self.assertTrue(timezone.is_aware(d.date))

        r = Deg.objects.filter(date__range=(t1, t0))
        self.assertTrue(len(r) == 2)

        chart = ArchiveChart(user=self.boss, start_date=t1, end_date=t0)
        dataset = chart.get_datasets('Deg')
        self.assertIsNotNone(dataset)
        values = self._extract_values(dataset)
        self.assertTrue(len(values) == 2)
        d1.delete()
        d2.delete()

    def test_get_first_day_of_week(self):
        first = timezone.datetime(2017, 10, 2)
        today1 = timezone.datetime(2017, 10, 8)
        self.assertEqual(CurrentWeekChart.get_first_day_of_week(today1), first)
        today2 = timezone.datetime(2017, 10, 7)
        self.assertEqual(CurrentWeekChart.get_first_day_of_week(today2), first)
        today3 = timezone.datetime(2017, 10, 3)
        self.assertEqual(CurrentWeekChart.get_first_day_of_week(today3), first)
        today4 = timezone.datetime(2017, 10, 2)
        self.assertEqual(CurrentWeekChart.get_first_day_of_week(today4), first)

    def test_chart_getdataset_for_user_this_week(self):
        chart = CurrentWeekChart(self.grone_user)
        tnow = timezone.localtime()
        first_day_of_week = CurrentWeekChart.get_first_day_of_week(tnow)
        tyesterday = timezone.datetime(day=first_day_of_week.day,
                                       month=first_day_of_week.month, year=first_day_of_week.year,
                                       hour=8)
        tyesterday = timezone.make_aware(tyesterday)
        d = Deg.objects.create(celsius=19.00, date=tyesterday, user=self.grone_user)
        dataset = chart.get_datasets(datatype='Deg')
        self.assertIsNotNone(dataset)
        values = self._extract_values(dataset)
        self.assertTrue(len(values) > 0)
        self.assertEqual(values[0]['y'], Decimal('19.000'))
        d.delete()

    def test_LastWeekChart(self):
        last_week_day = timezone.localtime() + timedelta(days=-7)
        t0 = ArchiveChart.get_first_day_of_week(last_week_day)
        # Starting at midnight sun
        t0 = t0 + timedelta(hours=-t0.hour, minutes=-t0.minute, seconds=-t0.second, microseconds=-t0.microsecond)
        some_days = [t0]
        day = t0
        for i in range(0, 6):
            day += timedelta(days=1)
            some_days.append(day)
        degs = []
        for day in some_days:
            deg_start = 18.00
            deg_hour_increment = 0.1
            start_time = day
            for i in range(0, 21):
                #print('start_time:', start_time)
                deg = Deg.objects.create(celsius=deg_start, user=self.boss, date=start_time)
                degs.append(deg)
                #print(deg)
                start_time += timedelta(hours=1)
                deg_start += deg_hour_increment
        # Testing the class
        chart = LastWeekChart(self.boss)
        dataset = chart.get_datasets('Deg')
        values = self._extract_values(dataset)
        self.assertTrue(len(values) > 0)
        for d in degs:
            d.delete()








    def test_get_today_data(self):
        """
        Getting data of the last hours starting from midnight.
        :return:
        """
        # Defining start of the day going back from current time.
        t = timezone.localtime()
        # Defining midnight of today.
        start_time = t + timedelta(hours=-t.hour, minutes=-t.minute, seconds=-t.second, microseconds=-t.microsecond)
        # Creating some measures every hour
        deg_start = 18.00
        deg_hour_increment = 0.1
        for i in range(0,13):
            deg = Deg.objects.create(celsius=deg_start, user=self.boss, date=start_time)
            start_time += timedelta(hours=1)
            deg_start += deg_hour_increment
            #print(deg)
        today_data =  Deg.objects.filter(date__day = 10, date__hour = 9)
        #print(today_data)






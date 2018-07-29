from django.test import TestCase
from phweb.models import Deg, Piscine, PiscineLog
from phweb.serializers import DegreeSerializer
from django.contrib.auth.models import User

class PiscineWatcherTest(TestCase):

    def setUp(self):

        deg_low = Deg.objects.create(celsius=12.25)
        deg_mid = Deg.objects.create(celsius=20.00)
        deg_high = Deg.objects.create(celsius=26.234)
        self.user_boss_passwd = 'titi_grognon234'
        self.user_boss = 'Boss'
        self.boss = User.objects.create_user(username=self.user_boss, password=self.user_boss_passwd,
                                             email='info@metacoherence.ch')
        self.piscine = Piscine.objects.create(user=self.boss, capacity=20000)

    def test_Deg(self):
        self.assertEqual(Deg.objects.count(), 3)

    def test_log(self):
        log = PiscineLog(piscine=self.piscine)
        log.msg = "Warning"
        self.assertIsNotNone(log.date)

    def test_serializer(self):
        serializer = DegreeSerializer()
        #print(repr(serializer))
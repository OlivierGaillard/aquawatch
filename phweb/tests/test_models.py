from django.test import TestCase
from phweb.models import Deg
from phweb.serializers import DegreeSerializer

class PiscineWatcherTest(TestCase):

    def setUp(self):

        deg_low = Deg.objects.create(celsius=12.25)
        deg_mid = Deg.objects.create(celsius=20.00)
        deg_high = Deg.objects.create(celsius=26.234)

    def test_Deg(self):
        self.assertEqual(Deg.objects.count(), 3)

    def test_serializer(self):
        serializer = DegreeSerializer()
        #print(repr(serializer))
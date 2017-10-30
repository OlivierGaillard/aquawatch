from .models import  Deg
from django.utils import timezone

def go():
    t0 = timezone.datetime(year=2016, month=1, day=1)
    t0 = timezone.make_aware(t0)
    tn = timezone.localtime()
    tn = timezone.datetime(year = 2016, month = tn.month, day = tn.day)
    tn = timezone.make_aware(tn)
    r = Deg.objects.filter(date__range = (t0, tn))
    n = 0
    for d in r:
        tn = d.date
        t17 = timezone.datetime(year=2017, month=tn.month, day=tn.day, hour=tn.hour, minute=tn.minutes, second = tn.seconds)
        t17 = timezone.make_aware(t17)
        #d17 = Degree.objects.create(celsius=d.celsius, date=t17, user=5)
        if n > 10:
            break

if __name__=='__main__':
    go()
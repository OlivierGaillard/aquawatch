from django.test import LiveServerTestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import RequestsClient, APIClient
import random
from phweb.models import Deg


class TestApi(LiveServerTestCase):
    """Cette classe permet de démontrer le fonctionnement des requêtes clientes REST avec
    l'authentification, la création des utilisateurs et des permissions. Elle utilise
    RequestsClient et APIClient (ce dernier avec un login). Elle test la récupération des
    données, l'envoi, la mise à jour et l'effacement. Seul les requêtes pour la class Deg sont
    testées. LiveServerTestCase permet d'utiliser une base de donnée toute neuve à chaque test."""

    def setUp(self):


        self.user_boss_passwd = 'titi_grognon234'
        self.user_boss = 'Boss'
        self.boss = User.objects.create_user(username=self.user_boss, password=self.user_boss_passwd,
                                             email='info@metacoherence.ch')

        deg_content_type = ContentType.objects.get_for_model(Deg)
        self.add_deg_perm = Permission.objects.get(codename = 'add_deg', content_type = deg_content_type,)
        self.del_deg_perm = Permission.objects.get(codename = 'delete_deg', content_type = deg_content_type)

        self.boss.user_permissions.add(self.add_deg_perm)
        self.boss.user_permissions.add(self.del_deg_perm)

        self.deg_low = Deg.objects.create(celsius=12.25, user=self.boss)
        self.deg_mid = Deg.objects.create(celsius=20.00, user=self.boss)
        self.deg_high = Deg.objects.create(celsius=26.234, user=self.boss)

        self.user_boss2 = 'Boss2'
        self.user_boss2_passwd = 'toto_grognon344'
        self.boss2 = User.objects.create_user(username=self.user_boss2, password=self.user_boss2_passwd,
                                             email='info@metablue.ch')
        self.boss2.user_permissions.add(self.add_deg_perm, self.del_deg_perm)
        self.deg_low2  = Deg.objects.create(celsius='13.245', user=self.boss2)
        self.deg_mid2  = Deg.objects.create(celsius='15.245', user=self.boss2)
        self.deg_high2 = Deg.objects.create(celsius='16.245', user=self.boss2)

    def test_user_created(self):
        user = User.objects.get(pk=self.boss.pk)
        self.assertEqual(user, self.boss)
        client = APIClient()
        r = client.login(username=self.user_boss, password=self.user_boss_passwd)
        self.assertTrue(r, 'login failed')
        client.logout()
        self.assertTrue(user.has_perm('phweb.add_deg'))
        self.assertTrue(user.has_perm('phweb.delete_deg'))



    def test_degree_list(self):
        client = RequestsClient()
        url = self.live_server_url + '/deg/'
        r = client.get(url, auth=(self.user_boss, self.user_boss_passwd))
        self.assertEqual(r.status_code, 200)
        results = r.json()
        self.assertEqual(type(results), list)
        self.assertTrue(len(results) > 0)
        last_result = results[0]
        self.assertEqual(last_result['celsius'], '26.234')



    def test_degree_post_with_RequestsClient(self):
        client = RequestsClient()
        url = self.live_server_url + '/deg/'
        json = {'celsius' : '16.00' }
        r = client.post(url, json=json, auth=(self.user_boss, self.user_boss_passwd))
        self.assertEqual(201, r.status_code)
        result = r.json()
        self.assertNotEqual('16.00', result['celsius'])
        self.assertEqual('16.000', result['celsius'])

    def test_degree_post_with_APIClient(self):
        client = APIClient()
        r = client.login(username=self.user_boss, password=self.user_boss_passwd)
        self.assertTrue(r, 'login failed')

        url = self.live_server_url + '/deg/'
        json = {'celsius' : '16.00' }
        r = client.post(url, json, format='json')
        self.assertEqual(201, r.status_code)
        result = r.json()
        self.assertNotEqual('16.00', result['celsius'])
        self.assertEqual('16.000', result['celsius'])
        client.logout()


    def test_degree_detail(self):
        """It is a shortcut for GET with the parameter pk."""
        last_deg = Deg.objects.filter(user=self.boss).last()
        client = RequestsClient()
        url = self.live_server_url + '/deg/%s/' % str(last_deg.pk)
        r = client.get(url, auth=(self.user_boss, self.user_boss_passwd))
        self.assertEqual(200, r.status_code)
        result = r.json()
        # We retrieve one measure contained in a dict
        self.assertEqual(type(result), dict)
        self.assertEqual(4, len(result))
        self.assertEqual(result['celsius'], str(last_deg.celsius))

    def test_last_measure_deg(self):
        last_deg = Deg.objects.filter(user=self.boss).last()
        client = RequestsClient()
        url = self.live_server_url + '/deg/last/'
        r = client.get(url, auth=(self.user_boss, self.user_boss_passwd))
        self.assertEqual(200, r.status_code)
        result = r.json()
        # We retrieve one measure contained in a dict
        self.assertEqual(type(result), dict)
        self.assertEqual(result['celsius'], str(last_deg.celsius))


    def test_degree_update(self):
        """This tests the update using a POST. The corresponding
        method is 'update_deg' from the same DegreeViewSet."""
        last_deg = Deg.objects.filter(user=self.boss).last()
        client = RequestsClient()
        url = self.live_server_url + '/deg/%s/update_deg/' % str(last_deg.pk)
        deg_value = random.randint(3, 30)
        deg_value += random.random()
        deg_str = "{0:.3f}".format(deg_value)
        r = client.post(url, {'celsius' : deg_str}, auth=(self.user_boss, self.user_boss_passwd))
        # getting the last measure
        deg = Deg.objects.get(pk=last_deg.pk)
        self.assertEqual(str(deg.celsius), deg_str)


    def test_delete(self):
        """If some value are bad measured we can delete it."""
        bad_degree = Deg.objects.create(celsius=3.333, user=self.boss)
        client = RequestsClient()
        url = self.live_server_url + '/deg/%s/delete/' % str(bad_degree.pk)
        r = client.post(url, auth=(self.user_boss, self.user_boss_passwd))
        self.assertEqual(r.status_code, 200)
        req = Deg.objects.filter(user=self.boss)

        self.assertEqual(req.count(), 3, "Got not 3 records but %s." % req.count())

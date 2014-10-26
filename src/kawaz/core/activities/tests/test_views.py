from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from activities.models import Activity
from activities.registry import registry
from activities.mediator import ActivityMediator
from kawaz.core.personas.models import Persona
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.core.activities.tests.factories import ActivityFactory

__author__ = 'giginet'

class ActivityViewTestCase(TestCase):

    def setUp(self):
        registry.register(Persona, ActivityMediator())

    def test_activities_activity_list_url(self):
        """
        name=activities_activity_listから/activities/を引ける
        """
        self.assertEqual(reverse('activities_activity_list'), '/activities/')

    def test_get_activities(self):
        """
        10件ずつActivityを取得できる
        """
        for i in range(15):
            PersonaFactory()
        r = self.client.get('/activities/')
        self.assertEqual(len(r.context['object_list']), 10)

        r = self.client.get('/activities/?page=2')
        self.assertEqual(len(r.context['object_list']), 10)
        self.assertIsNotNone(r.context['page_obj'])
        self.assertIsNotNone(r.context['paginator'])

    def test_get_latest_activities(self):
        """
         type=wallのとき、latestsの物だけを10件取得できる
        """
        for i in range(5):
            persona = PersonaFactory()
            persona.nickname = 'user{}'.format(i)
            persona.save()

        r = self.client.get('/activities/?type=wall')
        self.assertEqual(len(r.context['object_list']), 5)

        r = self.client.get('/activities/')
        self.assertEqual(len(r.context['object_list']), 10)

from django.test import TestCase
from model_mommy import mommy

from .models import Person, Connection


class PersonConnectionTest(TestCase):

    def setUp(self):
        mommy.make(Person, _quantity=10)
        self.persons = Person.objects.all()
        self.user = Person.objects.first()

    def test_total_person(self):
        self.assertEquals(10, self.persons.count())

    def test_add_connection_scenario(self):
        """User sent request 3 different user."""
        Connection.objects.bulk_create([
            Connection(person=self.user, friend=self.persons[3], status=Connection.REQUESTED),
            Connection(person=self.user, friend=self.persons[7], status=Connection.REQUESTED),
            Connection(person=self.user, friend=self.persons[8], status=Connection.REQUESTED),
        ])

        total_requested = Connection.objects.filter(person=self.user, status=Connection.REQUESTED)\
                                            .count()
        self.assertEquals(3, total_requested)

    def test_approve_connection_scenario(self):
        """User received 3 friend request and approve them."""
        Connection.objects.bulk_create([
            Connection(person=self.persons[4], friend=self.user, status=Connection.REQUESTED),
            Connection(person=self.persons[1], friend=self.user, status=Connection.REQUESTED),
            Connection(person=self.persons[6], friend=self.user, status=Connection.REQUESTED),
        ])

        friend_requests = Connection.objects.filter(friend=self.user, status=Connection.REQUESTED)
        self.assertEquals(3, friend_requests.count())

        # Approve all request.
        for connection in friend_requests:
            connection.status = Connection.APPROVED
            connection.save()

            # Check if reverse instance created.
            reversed_instance = Connection.objects.filter(person=self.user,
                                                          friend=connection.person,
                                                          status=Connection.APPROVED)

            # supposed to be exist and total count must be 1.
            self.assertEquals(1, reversed_instance.count())
            self.assertEquals(True, reversed_instance.exists())

    def test_unfriend_connection_scenario(self):
        """User unfriend one of their connections."""

        # Create friend request.
        Connection.objects.bulk_create([
            Connection(person=self.persons[4], friend=self.user, status=Connection.REQUESTED),
            Connection(person=self.persons[1], friend=self.user, status=Connection.REQUESTED),
            Connection(person=self.persons[6], friend=self.user, status=Connection.REQUESTED),
        ])

        # Approve all friend request.
        for i in Connection.objects.filter(friend=self.user, status=Connection.REQUESTED):
            i.status = Connection.APPROVED
            i.save()

        # Unfriend one of them.
        try:
            instance = Connection.objects.get(person=self.persons[4],
                                              friend=self.user,
                                              status=Connection.APPROVED)
        except Connection.DoesNotExist:
            pass
        else:
            instance.delete()

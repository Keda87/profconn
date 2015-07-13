from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError

from .models import Company


class CompanyTest(TestCase):

    def setUp(self):
        Company.objects.bulk_create([
            Company(name='Company I', employee_range=Company.EXTRA_SMALL,
                    founded=datetime(1997, 12, 10), address='Lawang Bedali 32',
                    email='hi@company1.com', phone='082776647455',
                    website='www.company1.com'),
            Company(name='Company II', employee_range=Company.MEDIUM,
                    founded=datetime(1998, 12, 10), address='Lawang Bedali 33',
                    email='admin@company2.com', phone='082776647455',
                    website='www.company1.com'),
            Company(name='Company III', employee_range=Company.XX_LARGE,
                    founded=datetime(1999, 12, 10), address='Lawang Bedali 34',
                    email='ask@company3.com', phone='082776647455',
                    website='www.company1.com')
        ])

    def test_create_company(self):
        companies = Company.objects.all()
        self.assertEquals(3, companies.count())

        new_company = Company.objects.create(name='Company IV',
                                             employee_range=Company.MEDIUM,
                                             founded=datetime(2011, 12, 10),
                                             address='Lawang Bedali 38',
                                             email='hello@company4.com',
                                             phone='08277664776',
                                             website='www.company4.com')
        self.assertEquals('Company IV', new_company.name)
        self.assertEquals(4, companies.count())

    def test_delete_company(self):
        company2 = Company.objects.get(name='Company II')
        self.assertEquals('Company II', company2.name)

        company2.delete()
        self.assertEquals(2, Company.objects.all().count())

    def test_update_company(self):
        company1 = Company.objects.get(name='Company I')
        self.assertEquals('Company I', company1.name)

        company1.name = 'Company 4'
        company1.save()
        self.assertEquals('Company 4', company1.name)

    def test_company_create_empty(self):
        with self.assertRaises(IntegrityError):
            Company.objects.create()

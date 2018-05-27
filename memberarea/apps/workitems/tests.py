from django.test import TestCase

from .models import RequiredHours


# Create your tests here.
class RequiredHoursTest(TestCase):
    
    def setUp(self):
        self.rhCollection = (
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=None),  # 00
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1900, toYearOfBirth=2000),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=2000),  # 02
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1900, toYearOfBirth=None),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1901, toYearOfBirth=None),  # 04
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=1901),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1950, toYearOfBirth=1970),  # 06
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1960, toYearOfBirth=None),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1971, toYearOfBirth=None),  # 08
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1971, toYearOfBirth=2000),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=None),  # 10
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=None),
        )

    def test_overlaps_with(self):

        # Overlap with it self must be True
        for rh in self.rhCollection:
            self.assertTrue(rh.overlaps_with(rh), msg="No self overlap")

        # Overlap with different year must be False
        dy_rh = RequiredHours(hours=0, missingHoursPrice=0, year=2018, fromYearOfBirth=None, toYearOfBirth=None)
        for rh in self.rhCollection:
            self.assertFalse(dy_rh.overlaps_with(rh), msg="Overlap for different years")

        self.assertEqual(self.rhCollection[0].overlaps_with(self.rhCollection[1]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[0].overlaps_with(self.rhCollection[2]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[0].overlaps_with(self.rhCollection[3]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[0].overlaps_with(self.rhCollection[4]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[0].overlaps_with(self.rhCollection[5]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[0].overlaps_with(self.rhCollection[6]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[0].overlaps_with(self.rhCollection[7]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[0].overlaps_with(self.rhCollection[8]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[7].overlaps_with(self.rhCollection[8]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[7].overlaps_with(self.rhCollection[9]), True,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[6].overlaps_with(self.rhCollection[8]), False,
                         msg="Overlap test failed")
        self.assertEqual(self.rhCollection[6].overlaps_with(self.rhCollection[9]), False,
                         msg="Overlap test failed")



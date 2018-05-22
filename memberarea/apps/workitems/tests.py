from django.test import TestCase

from .models import RequiredHours


# Create your tests here.
class RequiredHoursTest(TestCase):
    
    def setUp(self):
        self.rhCollection = (
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=None), # 00
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1900, toYearOfBirth=2000),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=2000), # 02
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1900, toYearOfBirth=None),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1901, toYearOfBirth=None), # 04
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=1901),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1950, toYearOfBirth=1970), # 06
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1960, toYearOfBirth=None),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1971, toYearOfBirth=None), # 08
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=1971, toYearOfBirth=2000),
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=None), # 10
            RequiredHours(hours=0, missingHoursPrice=0, year=2017, fromYearOfBirth=None, toYearOfBirth=None),
        )

    def test_overlapsWith(self):

        # Overlap with it self must be True
        for rh in self.rhCollection:
            self.assertTrue(rh.overlapsWith(rh), msg="No self overlap for: {}".format(rh))

        # Overlap with different year must be False
        dyRh = RequiredHours(hours=0, missingHoursPrice=0, year=2018, fromYearOfBirth=None, toYearOfBirth=None)
        for rh in self.rhCollection:
            self.assertFalse(dyRh.overlapsWith(rh), msg="Overlap for: {}".format(rh))

        self.assertEqual(self.rhCollection[0].overlapsWith(self.rhCollection[1]), True,
            msg="{} to {}".format(self.rhCollection[0], self.rhCollection[1]))
        self.assertEqual(self.rhCollection[0].overlapsWith(self.rhCollection[2]), True,
            msg="{} to {}".format(self.rhCollection[0], self.rhCollection[2]))
        self.assertEqual(self.rhCollection[0].overlapsWith(self.rhCollection[3]), True,
            msg="{} to {}".format(self.rhCollection[0], self.rhCollection[3]))
        self.assertEqual(self.rhCollection[0].overlapsWith(self.rhCollection[4]), True,
            msg="{} to {}".format(self.rhCollection[0], self.rhCollection[4]))
        self.assertEqual(self.rhCollection[0].overlapsWith(self.rhCollection[5]), True,
            msg="{} to {}".format(self.rhCollection[0], self.rhCollection[5]))
        self.assertEqual(self.rhCollection[0].overlapsWith(self.rhCollection[6]), True,
            msg="{} to {}".format(self.rhCollection[0], self.rhCollection[6]))
        self.assertEqual(self.rhCollection[0].overlapsWith(self.rhCollection[7]), True,
            msg="{} to {}".format(self.rhCollection[0], self.rhCollection[7]))
        self.assertEqual(self.rhCollection[0].overlapsWith(self.rhCollection[8]), True,
            msg="{} to {}".format(self.rhCollection[0], self.rhCollection[8]))
        self.assertEqual(self.rhCollection[7].overlapsWith(self.rhCollection[8]), True,
            msg="{} to {}".format(self.rhCollection[7], self.rhCollection[8]))
        self.assertEqual(self.rhCollection[7].overlapsWith(self.rhCollection[9]), True,
            msg="{} to {}".format(self.rhCollection[7], self.rhCollection[9]))
        self.assertEqual(self.rhCollection[6].overlapsWith(self.rhCollection[8]), False,
            msg="{} to {}".format(self.rhCollection[6], self.rhCollection[8]))
        self.assertEqual(self.rhCollection[6].overlapsWith(self.rhCollection[9]), False,
            msg="{} to {}".format(self.rhCollection[6], self.rhCollection[9]))



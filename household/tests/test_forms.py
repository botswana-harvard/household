from dateutil.relativedelta import relativedelta

from django.test import TestCase, tag
from model_mommy import mommy

from edc_constants.constants import YES

from ..constants import NO_HOUSEHOLD_INFORMANT
from ..exceptions import HouseholdAlreadyEnumeratedError, HouseholdAssessmentError
from ..forms import HouseholdAssessmentForm

from .test_mixins import HouseholdMixin


class TestForms(HouseholdMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.household_log_entry_set = self.make_household_with_household_log_entry(
            household_status=NO_HOUSEHOLD_INFORMANT)
        self.household_structure = (
            self.household_log_entry_set.all().first().household_log.household_structure)

    @tag('me1')
    def test_household_assessment_not_required_if_enumerated(self):
        household_structure = self.make_household_ready_for_enumeration()
        mommy.make_recipe(
            'member.representativeeligibility',
            household_structure=household_structure,
            report_datetime=self.get_utcnow())
#         mommy.make_recipe(
#             'member.householdmember',
#             household_structure=household_structure,
#             report_datetime=self.get_utcnow(),
#             )
#         self.assertRaises(
#             HouseholdAlreadyEnumeratedError,
#             mommy.make_recipe,
#             'household.householdassessment',
#             household_structure=household_structure,
#             report_datetime=self.get_utcnow())

    @tag('me')
    def test_household_assessment_not_required_if_insufficient_attempts(self):
        self.assertRaises(
            HouseholdAssessmentError,
            mommy.make_recipe,
            'household.householdassessment',
            household_structure=self.household_structure,
            report_datetime=self.get_utcnow())

    @tag('me')
    def test_household_assessment_potential_eligibles_yes(self):
        """Assert if eligibles_last_seen_home is not answered
        potential_eligibles is yes, error is raised."""
        self.make_household_log_entry(
            household_log=self.household_structure.householdlog,
            household_status=NO_HOUSEHOLD_INFORMANT,
            report_datetime=self.get_utcnow() + relativedelta(days=1))
        self.make_household_log_entry(
            household_log=self.household_structure.householdlog,
            household_status=NO_HOUSEHOLD_INFORMANT,
            report_datetime=self.get_utcnow() + relativedelta(days=2))
        self.assertGreaterEqual(self.household_structure.enumeration_attempts, 3)
        data = dict(
            household_structure=self.household_structure.id,
            report_datetime=self.get_utcnow() + relativedelta(days=2),
            potential_eligibles=YES,
            eligibles_last_seen_home=None)
        form = HouseholdAssessmentForm(data)
        self.assertFalse(form.is_valid())
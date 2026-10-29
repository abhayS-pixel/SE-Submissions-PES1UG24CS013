# Name : Abhay S
# SRN  : PES1UG24CS013
# Lab 6 - Branch coverage test cases for library_fines.py
# Every if / elif / else decision is driven to both True and False.

import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ---------- late_fine ----------

# Branch: member not in DAILY_FINE -> True
def test_unknown_member_raises():
    with pytest.raises(ValueError):
        late_fine("alumni", 5, False)


# Branch: days_kept < 0 -> True
def test_negative_days_raises():
    with pytest.raises(ValueError):
        late_fine("student", -1, False)


# Branch: days_kept < 0 -> False at boundary (0 days)
def test_zero_days_no_fine():
    assert late_fine("guest", 0, False) == 0


# Branch: member == "faculty" -> True, overdue > 0 -> False
def test_faculty_within_loan_period():
    assert late_fine("faculty", 30, False) == 0


# Branch: member == "faculty" -> True, overdue > 0 -> True, fine > 200 -> False
def test_faculty_overdue():
    assert late_fine("faculty", 35, False) == 5


# Branch: member == "faculty" -> False, overdue > 0 -> False (boundary 14 days)
def test_student_on_last_day():
    assert late_fine("student", 14, False) == 0


# Branch: overdue > 0 -> True (boundary 15 days), fine > 200 -> False
def test_student_one_day_late():
    assert late_fine("student", 15, False) == 2


# Branch: fine > 200 -> False at boundary (exactly 200)
def test_student_fine_exactly_200():
    # 114 days -> 100 overdue * 2 = 200, not capped
    assert late_fine("student", 114, False) == 200


# Branch: fine > 200 -> True (capped)
def test_guest_fine_capped():
    assert late_fine("guest", 100, False) == 200


# Branch: is_damaged -> True with no late fine
def test_damaged_on_time():
    assert late_fine("student", 5, True) == 150


# Branch: is_damaged -> True with capped late fine
def test_guest_capped_and_damaged():
    assert late_fine("guest", 100, True) == 350


# ---------- can_borrow ----------

# Branch: pending_fine > 100 -> True
def test_cannot_borrow_high_fine():
    assert can_borrow(0, 150, "student") is False


# Branch: pending_fine > 100 -> False at boundary (exactly 100)
def test_can_borrow_fine_exactly_100():
    assert can_borrow(0, 100, "student") is True


# Branch: member == "faculty" -> True, under limit
def test_faculty_can_borrow():
    assert can_borrow(9, 0, "faculty") is True


# Branch: member == "faculty" -> True, at limit
def test_faculty_at_limit():
    assert can_borrow(10, 0, "faculty") is False


# Branch: member == "faculty" -> False, under limit
def test_student_can_borrow():
    assert can_borrow(2, 0, "student") is True


# Branch: member == "faculty" -> False, at limit
def test_guest_at_limit():
    assert can_borrow(3, 0, "guest") is False


# ---------- renewal_status ----------

# Branch: has_reservation -> True
def test_renewal_denied_reservation():
    assert renewal_status(0, True, 5) == "denied"


# Branch: has_reservation -> False, times_renewed >= 2 -> True
def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


# Branch: times_renewed >= 2 -> False, days_left < 0 -> True
def test_renewal_overdue():
    assert renewal_status(1, False, -2) == "overdue"


# Branch: times_renewed >= 2 -> False, days_left < 0 -> False
def test_renewal_success():
    assert renewal_status(0, False, 5) == "renewed"


# Branch: days_left < 0 -> False at boundary (0 days left)
def test_renewal_on_due_date():
    assert renewal_status(1, False, 0) == "renewed"

# Name : Abhay S
# SRN  : PES1UG24CS013
# Lab 6 - Code (line) coverage test cases for library_fines.py

import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ---------- late_fine ----------

def test_returned_on_time():
    assert late_fine("student", 10, False) == 0


def test_unknown_member_raises():
    with pytest.raises(ValueError):
        late_fine("alumni", 5, False)


def test_negative_days_raises():
    with pytest.raises(ValueError):
        late_fine("student", -1, False)


def test_faculty_overdue():
    # 35 days kept, 30-day loan -> 5 days overdue * 1
    assert late_fine("faculty", 35, False) == 5


def test_guest_fine_capped_and_damaged():
    # 100 days kept, 14-day loan -> 86 * 5 = 430 -> capped at 200, +150 damage
    assert late_fine("guest", 100, True) == 350


# ---------- can_borrow ----------

def test_can_borrow():
    assert can_borrow(1, 0, "student") is True


def test_cannot_borrow_high_fine():
    assert can_borrow(0, 150, "student") is False


def test_faculty_can_borrow():
    assert can_borrow(5, 0, "faculty") is True


# ---------- renewal_status ----------

def test_renewal_denied_reservation():
    assert renewal_status(0, True, 5) == "denied"


def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


def test_renewal_overdue():
    assert renewal_status(1, False, -2) == "overdue"


def test_renewal_success():
    assert renewal_status(0, False, 5) == "renewed"

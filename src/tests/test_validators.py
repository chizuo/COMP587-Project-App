import pytest
from moviefinder.validators import EmailValidator
from moviefinder.validators import PasswordValidator
from PySide6 import QtGui


@pytest.mark.parametrize("email_address", ["bob@email.com", "bob@email.com.edu"])
def test_valid_email_addresses(email_address) -> None:
    v = EmailValidator()
    assert QtGui.QValidator.Acceptable == v.validate(email_address, 0)


@pytest.mark.parametrize(
    "not_email_address",
    [
        "",
        "bob",
        "bob@",
        "bob@email",
        "bob@email@.com",
        "@email.com",
        "bob.com",
    ],
)
def test_invalid_email_addresses(not_email_address) -> None:
    v = EmailValidator()
    assert QtGui.QValidator.Intermediate == v.validate(not_email_address, 0)


@pytest.mark.parametrize(
    "password",
    [
        "123456789",
        "wjoi1398fj9287%&LJjlkjg34k431LJK$#J%!jgoi4j#L$KJ42",
    ],
)
def test_valid_password(password) -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Acceptable == v.validate(password, 0)


def test_empty_password() -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Intermediate == v.validate("", 0)


def test_password_too_short() -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Intermediate == v.validate("12345678", 0)


def test_password_too_long() -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Invalid == v.validate(
        "wjoi1398fj9287%&LJjlkjg34k431LJK$#J%!jgoi4j#L$KJ42t", 0
    )

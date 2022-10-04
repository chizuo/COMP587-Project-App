import pytest
from PySide6 import QtGui

from src.moviefinder.validators import EmailValidator
from src.moviefinder.validators import PasswordValidator


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


@pytest.mark.parametrize(
    "not_password",
    [
        "12345678",
        "wjoi1398fj9287%&LJjlkjg34k431LJK$#J%!jgoi4j#L$KJ42t",
    ],
)
def test_invalid_password(not_password) -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Intermediate == v.validate(not_password, 0)

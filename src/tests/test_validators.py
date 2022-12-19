import pytest
from moviefinder.validators import EmailValidator
from moviefinder.validators import PasswordValidator
from PySide6 import QtGui


@pytest.mark.parametrize("email_address", ["bob@email.com", "bob@email.com.edu"])
def test_acceptable_email_addresses(email_address: str) -> None:
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
def test_intermediate_email_addresses(not_email_address: str) -> None:
    v = EmailValidator()
    assert QtGui.QValidator.Intermediate == v.validate(not_email_address, 0)


@pytest.mark.parametrize(
    "password",
    [
        "123456789",
        "wjoi1398fj9287%&LJjlkjg34k431LJK$#J%!jgoi4j#L$KJ42",
    ],
)
def test_acceptable_password(password: str) -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Acceptable == v.validate(password, 0)


@pytest.mark.parametrize(
    "not_password",
    [
        "",
        "12345678",
    ],
)
def test_intermediate_password(not_password: str) -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Intermediate == v.validate(not_password, 0)


@pytest.mark.parametrize(
    "not_password",
    [
        "wjoi1398fj9287%&LJjlkjg34k431LJK$#J%!jgoi4j#L$KJ42t",
    ],
)
def test_invalid_password(not_password: str) -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Invalid == v.validate(not_password, 0)

from types import ModuleType

import pytest
from moviefinder.buttons import add_services_groupbox
from moviefinder.service_name import ServiceName
from moviefinder.validators import EmailValidator
from moviefinder.validators import NameValidator
from moviefinder.validators import PasswordValidator
from moviefinder.validators import valid_services
from moviefinder.validators import valid_services_groupbox
from PySide6 import QtGui
from PySide6 import QtWidgets
from pytestqt import qtbot  # noqa: F401


@pytest.mark.parametrize("email_address", ["bob@email.com", "bob@email.com.edu"])
def test_acceptable_email_addresses(email_address: str) -> None:
    v = EmailValidator()
    assert QtGui.QValidator.Acceptable == v.validate(email_address)


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
    assert QtGui.QValidator.Intermediate == v.validate(not_email_address)


@pytest.mark.parametrize(
    "password",
    [
        "123456789",
        "wjoi1398fj9287%&LJjlkjg34k431LJK$#J%!jgoi4j#L$KJ42",
    ],
)
def test_acceptable_password(password: str) -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Acceptable == v.validate(password)


@pytest.mark.parametrize(
    "not_password",
    [
        "",
        "12345678",  # too short
    ],
)
def test_intermediate_password(not_password: str) -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Intermediate == v.validate(not_password)


@pytest.mark.parametrize(
    "not_password",
    [
        "wjoi1398fj9287%&LJjlkjg34k431LJK$#J%!jgoi4j#L$KJ42t",  # too long
    ],
)
def test_invalid_password(not_password: str) -> None:
    v = PasswordValidator()
    assert QtGui.QValidator.Invalid == v.validate(not_password)


@pytest.mark.parametrize(
    "name",
    [
        "a",
        "Bob",
        "Anne Jones",
        "李",
    ],
)
def test_acceptable_name(name: str) -> None:
    v = NameValidator()
    assert QtGui.QValidator.Acceptable == v.validate(name)


def test_intermediate_name() -> None:
    v = NameValidator()
    assert QtGui.QValidator.Intermediate == v.validate("")


@pytest.mark.parametrize(
    "services",
    [
        {
            ServiceName.AMAZON_PRIME: "https://www.amazon.com/gp/video/detail/B09WVCGMT3/ref=atv_hm_hom_3_c_QDWBgv_brws_3_3"  # noqa: E501
        },
        {
            ServiceName.APPLE_TV_PLUS: "https://tv.apple.com/us/movie/emancipation/umc.cmc.1j6fdxookwtqml3bd8ivvcbbv?ctx_brand=tvs.sbd.4000"  # noqa: E501
        },
        {ServiceName.DISNEY_PLUS: "https://www.disneyplus.com/welcome/andor"},
        {
            ServiceName.HULU: "https://www.hulu.com/movie/1dd27c8e-8e1f-443b-8bd1-6066e5237d8b"  # noqa: E501
        },
        {ServiceName.NETFLIX: "https://www.netflix.com/title/80196613/"},
        {
            ServiceName.HULU: "https://www.hulu.com/movie/5387fb0a-a16e-4118-a244-31056c6d396c",  # noqa: E501
            ServiceName.NETFLIX: "https://www.netflix.com/title/80236421/",
        },
    ],
)
def test_valid_services(services: dict[ServiceName, str]) -> None:
    assert valid_services(services)


@pytest.mark.parametrize(
    "not_services",
    [
        {
            ServiceName.APPLE_TV_PLUS: "https://apple.com/us/movie/emancipation/umc.cmc.1j6fdxookwtqml3bd8ivvcbbv?ctx_brand=tvs.sbd.4000"  # noqa: E501
        },
        {ServiceName.APPLE_TV_PLUS: "https://www.zombo.com"},
        {ServiceName.DISNEY_PLUS: "https://www.disney.com/welcome/andor"},
        {ServiceName.AMAZON_PRIME: ""},
    ],
)
def test_invalid_services(not_services: dict[ServiceName, str]) -> None:
    assert not valid_services(not_services)


def test_valid_services_groupbox_none_checked(qtbot: ModuleType) -> None:  # noqa: F811
    w = QtWidgets.QWidget()
    w.layout = QtWidgets.QFormLayout(w)
    add_services_groupbox(w)
    assert not valid_services_groupbox(w.services_group_box)


def test_valid_services_groupbox_one_checked(qtbot: ModuleType) -> None:  # noqa: F811
    w = QtWidgets.QWidget()
    w.layout = QtWidgets.QFormLayout(w)
    add_services_groupbox(w)
    w.disney_plus_checkbox.setChecked(True)
    assert valid_services_groupbox(w.services_group_box)


def test_valid_services_groupbox_all_checked(qtbot: ModuleType) -> None:  # noqa: F811
    w = QtWidgets.QWidget()
    w.layout = QtWidgets.QFormLayout(w)
    add_services_groupbox(w)
    w.amazon_prime_checkbox.setChecked(True)
    w.apple_tv_plus_checkbox.setChecked(True)
    w.disney_plus_checkbox.setChecked(True)
    w.hulu_checkbox.setChecked(True)
    w.netflix_checkbox.setChecked(True)
    assert valid_services_groupbox(w.services_group_box)

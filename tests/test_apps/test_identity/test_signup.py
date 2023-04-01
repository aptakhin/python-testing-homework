from http import HTTPStatus
from typing import TYPE_CHECKING
from django.http import HttpResponse

import pytest
from django.test import Client
from django.urls import reverse

if TYPE_CHECKING:
    from tests.plugins.identity.pytest_identity import (
        ExpectedUserData,
        MockLeadFetchAPI,
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
    )


@pytest.mark.django_db()
def test_valid_registration_mock(
    client: Client,
    registration_data: 'RegistrationData',
    expected_user_data: 'ExpectedUserData',
    assert_correct_user: 'UserAssertion',
    mock_lead_post_user_api: 'MockLeadFetchAPI',
) -> None:
    """Test that registration works with correct user data."""
    with mock_lead_post_user_api():
        response: HttpResponse = client.post(
            reverse('identity:registration'),
            data=registration_data,
        )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:login')  # type: ignore[attr-defined]
    assert_correct_user(
        registration_data['email'],
        expected_user_data(registration_data),
    )


@pytest.mark.django_db()
@pytest.mark.timeout(3)
def test_valid_registration(
    client: Client,
    registration_data: 'RegistrationData',
    expected_user_data: 'ExpectedUserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with correct user data."""
    response: HttpResponse = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:login')  # type: ignore[attr-defined]
    assert_correct_user(
        registration_data['email'],
        expected_user_data(registration_data),
    )


@pytest.mark.django_db()
def test_invalid_registration_no_email(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    """Test invalid registration with no email."""
    user_data = registration_data_factory()
    user_data.pop('email')
    response: HttpResponse = client.post(
        reverse('identity:registration'),
        data=user_data,
    )

    assert response.status_code == HTTPStatus.OK  # not HTTPStatus.FOUND


@pytest.mark.django_db()
def test_invalid_registration_invalid_email(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    """Test invalid registration with invalid email."""
    response: HttpResponse = client.post(
        reverse('identity:registration'),
        data=registration_data_factory(email='invalid'),
    )

    assert response.status_code == HTTPStatus.OK  # not HTTPStatus.FOUND

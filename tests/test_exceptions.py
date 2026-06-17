# -*- coding: utf-8 -*-
'''
Tests for the exception hierarchy and its backward compatibility.
'''

import pytest

from icinga2apic.exceptions import (
    Icinga2ApiException,
    Icinga2ApiRequestException,
    Icinga2ApiProxyException,
    Icinga2ApiClientException,
    Icinga2ApiHttpException,
    Icinga2ApiTimeoutException,
    Icinga2ApiConfigFileException,
)


REQUEST_SUBCLASSES = (
    Icinga2ApiProxyException,
    Icinga2ApiClientException,
    Icinga2ApiHttpException,
    Icinga2ApiTimeoutException,
)


class _Resp(object):
    def __init__(self, text, payload=None, raises=False):
        self.text = text
        self._payload = payload
        self._raises = raises

    def json(self):
        if self._raises:
            raise ValueError("no json")
        return self._payload


@pytest.mark.parametrize("cls", REQUEST_SUBCLASSES)
def test_request_errors_are_children_of_request_exception(cls):
    # backward compatibility: 'except Icinga2ApiRequestException' must keep
    # catching every kind of request failure.
    assert issubclass(cls, Icinga2ApiRequestException)
    assert issubclass(cls, Icinga2ApiException)


def test_config_file_exception_is_api_exception():
    assert issubclass(Icinga2ApiConfigFileException, Icinga2ApiException)


def test_base_request_exception_keeps_legacy_attributes():
    exc = Icinga2ApiProxyException("POST", "http://example/x")
    # .response default kept for backward compatibility (empty for non-HTTP)
    assert exc.response == {}
    # .error attribute preserved on the base class
    assert exc.error == str(exc)
    assert exc.method == "POST"
    assert exc.url == "http://example/x"


def test_http_exception_with_json_body():
    exc = Icinga2ApiHttpException(
        "GET", "http://example/x", 503, _Resp('{"err": 1}', {"err": 1}))
    assert exc.status_code == 503
    assert exc.response == {"err": 1}
    assert isinstance(exc, Icinga2ApiRequestException)


def test_http_exception_with_non_json_body_does_not_crash():
    exc = Icinga2ApiHttpException(
        "GET", "http://example/x", 502, _Resp("<html>502</html>", raises=True))
    assert exc.status_code == 502
    assert exc.response == {}


def test_catch_compat_covers_all_subclasses():
    errors = [
        Icinga2ApiProxyException("POST", "u"),
        Icinga2ApiClientException("POST", "u", RuntimeError("x")),
        Icinga2ApiTimeoutException("POST", "u", 5),
        Icinga2ApiHttpException("GET", "u", 500, _Resp("{}", {})),
    ]
    for err in errors:
        with pytest.raises(Icinga2ApiRequestException):
            raise err

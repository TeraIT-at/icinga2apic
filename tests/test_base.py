# -*- coding: utf-8 -*-
'''
Tests for request error wrapping, timeout and certificate verification in Base.
'''

import requests
import pytest

from icinga2apic.base import Base
from icinga2apic.exceptions import (
    Icinga2ApiProxyException,
    Icinga2ApiClientException,
    Icinga2ApiTimeoutException,
    Icinga2ApiHttpException,
)


class _Manager(object):
    url = "http://h/"
    version = "test"
    certificate = None
    key = None
    ca_certificate = None
    username = None
    password = None
    timeout = 5
    validate_certs = False


class _FakeSession(object):
    '''A session whose post() either raises or returns a canned response.'''

    def __init__(self, raise_exc=None, response=None, captured=None):
        self.headers = {}
        self.cert = None
        self.auth = None
        self._raise = raise_exc
        self._response = response
        self._captured = captured if captured is not None else {}

    def post(self, **kwargs):
        self._captured.update(kwargs)
        if self._raise is not None:
            raise self._raise
        return self._response

    def close(self):
        pass


def _base_with(session, manager=None):
    base = Base(manager or _Manager())
    base._create_session = lambda method='POST': session
    return base


@pytest.mark.parametrize("raised, expected", [
    (requests.exceptions.ProxyError("p"), Icinga2ApiProxyException),
    # ConnectTimeout is also a ConnectionError -> must be classified as timeout
    (requests.exceptions.ConnectTimeout("t"), Icinga2ApiTimeoutException),
    (requests.exceptions.ReadTimeout("t"), Icinga2ApiTimeoutException),
    (requests.exceptions.ConnectionError("c"), Icinga2ApiClientException),
])
def test_request_errors_are_wrapped(raised, expected):
    base = _base_with(_FakeSession(raise_exc=raised))
    with pytest.raises(expected):
        base._request("POST", "v1/x", {"a": 1})


def test_timeout_and_verify_passed_to_requests():
    captured = {}
    base = _base_with(_FakeSession(
        raise_exc=requests.exceptions.ProxyError("p"), captured=captured))
    with pytest.raises(Icinga2ApiProxyException):
        base._request("POST", "v1/x")
    assert captured["timeout"] == 5
    assert captured["verify"] is False


def test_verify_true_when_validate_certs_enabled():
    manager = _Manager()
    manager.validate_certs = True
    captured = {}
    base = _base_with(
        _FakeSession(raise_exc=requests.exceptions.ProxyError("p"),
                     captured=captured),
        manager=manager)
    with pytest.raises(Icinga2ApiProxyException):
        base._request("POST", "v1/x")
    assert captured["verify"] is True


def test_non_2xx_raises_http_exception():
    class _Resp(object):
        status_code = 404
        text = '{"e": 1}'
        url = "http://h/v1/x"

        def json(self):
            return {"e": 1}

    base = _base_with(_FakeSession(response=_Resp()))
    with pytest.raises(Icinga2ApiHttpException) as info:
        base._request("POST", "v1/x")
    assert info.value.status_code == 404
    assert info.value.response == {"e": 1}

# -*- coding: utf-8 -*-
'''
Tests for the lazy subscribe() vs. eager subscribe_now() behaviour.
'''

from icinga2apic.events import Events


class _Manager(object):
    url = "http://h/"
    version = "test"
    certificate = None
    key = None
    ca_certificate = None
    username = None
    password = None
    timeout = None
    validate_certs = False


def _events_with_recorder():
    events = Events(_Manager())
    calls = []

    def fake_request(method, path, payload, stream=False):
        calls.append(payload)
        return object()

    events._request = fake_request
    events._get_message_from_stream = lambda stream: iter(["a", "b"])
    return events, calls


def test_subscribe_is_lazy():
    events, calls = _events_with_recorder()
    generator = events.subscribe(["CheckResult"], "q", filters="f")
    # nothing requested until first iteration
    assert calls == []
    first = next(generator)
    assert first == "a"
    assert len(calls) == 1
    assert calls[0] == {"types": ["CheckResult"], "queue": "q", "filter": "f"}


def test_subscribe_now_is_eager():
    events, calls = _events_with_recorder()
    generator = events.subscribe_now(["CheckResult"], "q", filters="f")
    # request already sent before any iteration
    assert len(calls) == 1
    assert list(generator) == ["a", "b"]

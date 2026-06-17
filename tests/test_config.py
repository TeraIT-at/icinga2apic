# -*- coding: utf-8 -*-
'''
Tests for config file parsing of the new typed options.
'''

import tempfile
import os

import pytest

from icinga2apic.configfile import ClientConfigFile


BASE = "[api]\nurl = https://h:5665\nusername = u\npassword = p\n"


def _parse(body):
    fd, path = tempfile.mkstemp(suffix=".ini")
    os.write(fd, body.encode())
    os.close(fd)
    try:
        cfg = ClientConfigFile(path)
        cfg.parse()
        return cfg
    finally:
        os.unlink(path)


def test_validate_certs_false_is_boolean_not_truthy_string():
    # regression: 'false' must not be parsed as the truthy string "false"
    cfg = _parse(BASE + "validate_certs = false\n")
    assert cfg.validate_certs is False


def test_validate_certs_true():
    cfg = _parse(BASE + "validate_certs = true\n")
    assert cfg.validate_certs is True


def test_validate_certs_absent_is_none():
    cfg = _parse(BASE)
    assert cfg.validate_certs is None


def test_timeout_parsed_as_float():
    cfg = _parse(BASE + "timeout = 10\n")
    assert cfg.timeout == pytest.approx(10.0)
    assert isinstance(cfg.timeout, float)

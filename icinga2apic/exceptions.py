# -*- coding: utf-8 -*-
'''
Copyright 2017 fmnisme@gmail.com, Copyright 2020 christian@jonak.org

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Icinga 2 API client exceptions
'''

class Icinga2ApiException(Exception):
    '''
    Icinga 2 API base exception class
    '''

    def __init__(self, error):
        super(Icinga2ApiException, self).__init__(error)
        self.error = error

    def __str__(self):
        return str(self.error)


class Icinga2ApiRequestException(Icinga2ApiException):
    '''
    Icinga 2 API request exception class

    Base class for every error that can occur while performing a request.
    More specific subclasses carry additional context (e.g. the HTTP status
    code or the timeout value). Catching this class keeps catching every
    request failure, as before.
    '''

    # kept for backward compatibility: consumers may read ``.response`` even
    # for non-HTTP errors, where it stays an empty dict.
    response = {}

    def __init__(self, method, url, error):
        super(Icinga2ApiRequestException, self).__init__(error)
        self.method = method
        self.url = url


class Icinga2ApiProxyException(Icinga2ApiRequestException):
    '''
    Icinga 2 API HTTP connection to proxy server failed.
    '''

    def __init__(self, method, url):
        super(Icinga2ApiProxyException, self).__init__(
            method,
            url,
            "Request {} {} failed: Unable to connect to proxy.".format(
                method, url),
        )


class Icinga2ApiClientException(Icinga2ApiRequestException):
    '''
    Icinga 2 API HTTP connection error.
    '''

    def __init__(self, method, url, exception):
        super(Icinga2ApiClientException, self).__init__(
            method, url,
            "Request {} {} failed: {}".format(method, url, exception),
        )


class Icinga2ApiHttpException(Icinga2ApiRequestException):
    '''
    Icinga 2 API request returned a non-2xx HTTP status code.
    '''

    def __init__(self, method, url, status_code, response):
        super(Icinga2ApiHttpException, self).__init__(
            method,
            url,
            "Request {} {} failed with status code {}: {}".format(
                method, url, status_code, response.text
            ),
        )
        self.status_code = status_code
        try:
            self.response = response.json()
        except ValueError:
            # response body is not valid JSON (e.g. an HTML error page)
            self.response = {}


class Icinga2ApiTimeoutException(Icinga2ApiRequestException):
    '''
    Icinga 2 API request timed out.
    '''

    def __init__(self, method, url, timeout):
        super(Icinga2ApiTimeoutException, self).__init__(
            method,
            url,
            "Request {} {} timed out after {} seconds.".format(
                method, url, timeout),
        )
        self.timeout = timeout


class Icinga2ApiConfigFileException(Icinga2ApiException):
    '''
    Icinga 2 API config file exception class
    '''

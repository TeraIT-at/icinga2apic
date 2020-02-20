from setuptools import setup

PACKAGE = "icinga2apic"
NAME = "icinga2apic"
DESCRIPTION = "Python Icinga 2 API - Continued"
AUTHOR = "Christian Jonak-Möchel, fmnisme, Tobias von der Krone"
AUTHOR_EMAIL = "christian@jonak.org, fmnisme@gmail.com, tobias@vonderkrone.info"
URL = "https://github.com/joni1993/icinga2apic"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=["requests"],
    keywords="Icinga api",
    license="2-Clause BSD",
    url=URL,
    packages=[PACKAGE],
    zip_safe=False,
    long_description=open("README.md").read(),
)

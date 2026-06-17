# CHANGELOG

<!-- version list -->

## v0.8.0 (2026-06-17)

### Build System

- **release**: Migrate semantic-release to pyproject, add local release flow
  ([`319eb03`](https://github.com/joni1993/icinga2apic/commit/319eb03f8c4f7a08d38dee2a4925a67717388d65))

- **release**: Unify release/versioning setup with check_paloalto_ng
  ([`8117588`](https://github.com/joni1993/icinga2apic/commit/8117588d3c3d01eedc2663c9a9ea9e57bdcaa18f))

### Chores

- **build**: Drop redundant version from setup.cfg
  ([`9d44965`](https://github.com/joni1993/icinga2apic/commit/9d44965d6cf8db8e23f08372fc114fdb2e1d6d94))

### Continuous Integration

- Align test workflow with sibling project (lint job + Python 3.9-3.14)
  ([`c68aafa`](https://github.com/joni1993/icinga2apic/commit/c68aafa7750deb4e77956f166a8751c8673832a1))

- Run tests across Python 3.8-3.12
  ([`048220a`](https://github.com/joni1993/icinga2apic/commit/048220a0fa5cd1cf412e20b750a30510e9ec4971))

### Documentation

- Document testing and release process
  ([`95a74fc`](https://github.com/joni1993/icinga2apic/commit/95a74fc888b2a6eee51e65220e28ffc1aff926c0))

### Features

- **actions**: Allow optional author for remove_downtime
  ([#9](https://github.com/joni1993/icinga2apic/pull/9),
  [`fb03c6c`](https://github.com/joni1993/icinga2apic/commit/fb03c6c05dbfa7029c99c85549ab15d09d29f5e5))

- **events**: Add eager subscribe_now() alongside lazy subscribe()
  ([#7](https://github.com/joni1993/icinga2apic/pull/7),
  [`e8a13e4`](https://github.com/joni1993/icinga2apic/commit/e8a13e487b338b848a1955176faccdce4dd4a8b8))

- **exceptions**: Specific request exceptions, honor timeout, add validate_certs
  ([#10](https://github.com/joni1993/icinga2apic/pull/10),
  [`df7bda0`](https://github.com/joni1993/icinga2apic/commit/df7bda0fdec4b2fdc87f26024b4ae666ebe66b3e))

### Testing

- Add pytest smoke test suite
  ([`f1a0331`](https://github.com/joni1993/icinga2apic/commit/f1a0331a36490c230d1ca34c601bb1adde7393a0))


## v0.7.5 (2022-04-24)
### Feature
* **actions:** Support filters for process-check-result (fixes #4) ([`12be4c5`](https://github.com/joni1993/icinga2apic/commit/12be4c5f862b1af7f58b97ad25d7bb73f56b3db4))

### Fix
* **encoding:** Remove umlaut from name ([`d964e1d`](https://github.com/joni1993/icinga2apic/commit/d964e1d978e4c8d137edd501f4aa19040d10cb8e))
* **actions:** Allow to remove comments based on filter  ([`a74120f`](https://github.com/joni1993/icinga2apic/commit/a74120f9da026bf20383d644fdc88dc15b16b309))

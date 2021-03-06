# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

For detailed code changes, please visit
https://github.com/greenbone/hyperion/commits/master
or get the entire source code repository and view log history:

```sh
$ git clone https://github.com/greenbone/hyperion.git
$ cd hyperion && git log
```

## [Unreleased]

### Added

- Introduced new base classes for queries [#126](https://github.com/greenbone/hyperion/pull/126)
- Use [#graphdoc](https://github.com/wallee94/graphdoc) as schema documentation tool [#124](https://github.com/greenbone/hyperion/pull/124)
- Add csv_to_list function [#96](https://github.com/greenbone/hyperion/pull/96)
- Add `new_severity` to override mutations [#85](https://github.com/greenbone/hyperion/pull/85)
- Query for target tasks in single query [#78](https://github.com/greenbone/hyperion/pull/78)
- Add `owner`, `detection_result`, `notes`, `tickets` and `user_tags` for result fields [#69](https://github.com/greenbone/hyperion/pull/69)
- Support credential download and add fields to Credential [#66](https://github.com/greenbone/hyperion/pull/66)
- Add `compliance_count` to AuditLastReport [#26](https://github.com/greenbone/hyperion/pull/26)
- Implement `average_duration` for tasks and audits fields. [#14](https://github.com/greenbone/hyperion/pull/14)
- Implement new abstract Class for SecInfo BulkExport by IDs. [#24](https://github.com/greenbone/hyperion/pull/24)
- Add Bulk Export for NVTs. [#25](https://github.com/greenbone/hyperion/pull/25)

### Changed
- `getPreference(s)` is now divided into `getScanConfigPreference(s)` and `getNvtPreference(s)` [#168](https://github.com/greenbone/hyperion/pull/168)
- Revisit audit and task object types [#133](https://github.com/greenbone/hyperion/pull/133), [#149](https://github.com/greenbone/hyperion/pull/149), [#150](https://github.com/greenbone/hyperion/pull/150)
- Revisit authentication methods [#93](https://github.com/greenbone/hyperion/pull/93)
- Revisit port list object type, queries and mutations [#108](https://github.com/greenbone/hyperion/pull/108)
- Revisit feed status object types [#95](https://github.com/greenbone/hyperion/pull/95), [#122](https://github.com/greenbone/hyperion/pull/122)
- Introduce QoDType enum and use common QoD class for NVT and Result [#109](https://github.com/greenbone/hyperion/pull/109)
- Revisit result object type [#92](https://github.com/greenbone/hyperion/pull/92)
- Revisit target object type, queries and mutations 
  [#97](https://github.com/greenbone/hyperion/pull/97),
  [#106](https://github.com/greenbone/hyperion/pull/106),
  [#113](https://github.com/greenbone/hyperion/pull/113)
- Explicitly implement audit subobjects [#26](https://github.com/greenbone/hyperion/pull/26)
- For all NVT related Entities we use `id` instead of `oid` now, so every Entity uses `id` now. [#15](https://github.com/greenbone/hyperion/pull/15)
- Use `next` instead of `latest` `python-gvm` version for development. [#15](https://github.com/greenbone/hyperion/pull/15)
- Removed empty `uuid= ` from `filter_string` in `create_export_by_ids_mutation` [#23](https://github.com/greenbone/hyperion/pull/23)
- Changed dependency of `xml` to `lxml` [#27](https://github.com/greenbone/hyperion/pull/27)
- Changed `CVE`s entity so it can parse new-format xml correctly [#29](https://github.com/greenbone/hyperion/pull/29) [#38](https://github.com/greenbone/hyperion/pull/38)
- Refactored `OvalDefinitions` entity [#30](https://github.com/greenbone/hyperion/pull/30)
- Increased coverage for `OvalDefinitions`, `CertBundAdvisories` and `DFNCertAdvisories` entity [#30](https://github.com/greenbone/hyperion/pull/30)
- Added the `deprecatedBy` field to `CPEs` [#51](https://github.com/greenbone/hyperion/pull/51)
- Refactored `NVT` entity, removed complexity and redundant fields [#58](https://github.com/greenbone/hyperion/pull/58)[#60](https://github.com/greenbone/hyperion/pull/60)[#64](https://github.com/greenbone/hyperion/pull/64)
- Improved GraphQL schema [#83](https://github.com/greenbone/hyperion/pull/83)

### Deprecated

### Removed
- BulkDeleteByReport (for Hosts and OperatingSystems) [#168](https://github.com/greenbone/hyperion/pull/168)
- Remove OVAL definitions from the schema [#136](https://github.com/greenbone/hyperion/pull/136)
- Remove our sphinx extension for documenting the GraphQL schema [#123](https://github.com/greenbone/hyperion/pull/123)

### Fixed

- Fixed crash if targets of a port list have been created from a post list without targets [#134](https://github.com/greenbone/hyperion/pull/134)
- Fixed a problem with NVT `oid` in Notes. [#15](https://github.com/greenbone/hyperion/pull/15)
- Fixed a problem with NVT `oid` in Overrides. [#16](https://github.com/greenbone/hyperion/pull/16)
- Now the `name` field in Overrides and Notes can not be queried. It returned the `name` of the `permission`/`owner` because of `.find()`. Notes/Overrides don't have a name field theirself. [#16](https://github.com/greenbone/hyperion/pull/16)
- Added the `asset_hosts_filter` parameter to `createTarget` mutation [#15](https://github.com/greenbone/hyperion/pull/15)
- Added the `allow_simultaneous_ips` parameter to `createTarget`, `modifyTarget` mutation and `getTarget(s)` queries. [#15](https://github.com/greenbone/hyperion/pull/15)
- Fixed `FutureWarnings` due to `if x:` -> `if x is not None:` [#27](https://github.com/greenbone/hyperion/pull/27)
- Added missing fields to `CPE` entity [#39](https://github.com/greenbone/hyperion/pull/39)
- Fix product rstrip() from NoneType error. [#41](https://github.com/greenbone/hyperion/pull/41)
- Adding missing field `port` to `override` entity. [#57](https://github.com/greenbone/hyperion/pull/57)
- Improved `Report` Entity, fixed and tested `ReportError` [65](https://github.com/greenbone/hyperion/pull/65)
- Split `ScannerPreferences` and `NVTPreferences` in `ScanConfigs` and `Policies` [67](https://github.com/greenbone/hyperion/pull/67)

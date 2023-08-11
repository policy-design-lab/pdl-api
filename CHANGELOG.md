# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Crop Insurance endpoints. [#78](https://github.com/policy-design-lab/pdl-api/issues/78)

### Changed
- EQIP data based on latest information. [#97](https://github.com/policy-design-lab/pdl-api/issues/97)
- Title 1 Commodities JSON files. [#99](https://github.com/policy-design-lab/pdl-api/issues/99)
- Title 1 Commodities JSON files after raw data update. [#110](https://github.com/policy-design-lab/pdl-api/issues/110)

### Fixed
- API endpoints returns json without soring orders. [#101](https://github.com/policy-design-lab/pdl-api/issues/101)
- Title 1 Commodities state distribution JSON file. [#104](https://github.com/policy-design-lab/pdl-api/issues/104)
- Title 1 Commodities state distribution JSON to use correct average payee counts. [#112](https://github.com/policy-design-lab/pdl-api/issues/112)

## [0.4.0] - 2023-06-08

### Changed
- SNAP data based on latest information. [#91](https://github.com/policy-design-lab/pdl-api/issues/91)

## [0.3.0] - 2023-05-26

### Added
- Title I Commodities json GET endpoints. [#40](https://github.com/policy-design-lab/pdl-api/issues/40)

### Changed
- Make summary and all programs directly served from json file. [#65](https://github.com/policy-design-lab/pdl-api/issues/65)

### Fixed
- Topline numbers for crop insurance and re-calculated total payments. [#81](https://github.com/policy-design-lab/pdl-api/issues/81)

## [0.2.0] - 2023-05-10

### Added
- Statute-level percentages to CSP JSON data. [#71](https://github.com/policy-design-lab/pdl-api/issues/71)

### Changed
- Update CSP JSON data files. [#61](https://github.com/policy-design-lab/pdl-api/issues/61)
- Update EQIP JSON data files. [#53](https://github.com/policy-design-lab/pdl-api/issues/53)
- Pastured cropland with Grassland in CSP JSON files. [#73]https://github.com/policy-design-lab/pdl-api/issues/73
- Database update script upgraded to sqlalchemy 2 or higher. [#28](https://github.com/policy-design-lab/pdl-api/issues/28)
- Updated syntax for summary end point. [#67](https://github.com/policy-design-lab/pdl-api/issues/67)

### Fixed
- CSP JSON file by adding zero entries for soil testing. [#69](https://github.com/policy-design-lab/pdl-api/issues/69)

## [0.1.0] - 2023-04-18

### Added
- Create repository. [#1](https://github.com/policy-design-lab/pdl-api/issues/1)
- Create database. [#3](https://github.com/policy-design-lab/pdl-api/issues/3)
- Endpoints for summary, state, and all programs. [#7](https://github.com/policy-design-lab/pdl-api/issues/7)
- Search option for existing endpoints. [#11](https://github.com/policy-design-lab/pdl-api/issues/11)
- Docker container. [#12](https://github.com/policy-design-lab/pdl-api/issues/12)
- GitHub action for automated container build. [#13](https://github.com/policy-design-lab/pdl-api/issues/13)
- Statecode endpoint in the endpoint. [#15](https://github.com/policy-design-lab/pdl-api/issues/15)
- Created statecode table in database. [#16](https://github.com/policy-design-lab/pdl-api/issues/16)
- CORS for developing with frontend. [#20](https://github.com/policy-design-lab/pdl-api/issues/20)
- Format test function for the PEP8 formatting. [#24](https://github.com/policy-design-lab/pdl-api/issues/24)

### Changed
- EQIP json GET endpoints. [#35](https://github.com/policy-design-lab/pdl-api/issues/35)
- SNAP json GET endpoints. [#42](https://github.com/policy-design-lab/pdl-api/issues/42)
- Title II CSP json GET endpoints. [#45](https://github.com/policy-design-lab/pdl-api/issues/45)
- Update SNAP JSON file structure and add participation percentages. [#48](https://github.com/policy-design-lab/pdl-api/issues/48)

### Fixed
- Open API sepecification file. [#50](https://github.com/policy-design-lab/pdl-api/issues/50)

[0.4.0]: https://github.com/policy-design-lab/pdl-api/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/policy-design-lab/pdl-api/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/policy-design-lab/pdl-api/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/policy-design-lab/pdl-api/releases/tag/0.1.0

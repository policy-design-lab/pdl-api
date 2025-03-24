# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

### Added
- Add year query parameter to Crop Insurance endpoints. [#302](https://github.com/policy-design-lab/pdl-api/issues/302)

## [0.22.0] - 2025-02-26

### Added
- Add back summary endpoint to SNAP. [#271](https://github.com/policy-design-lab/pdl-api/issues/271)
- Add top-level endpoints to Title-II. [#270](https://github.com/policy-design-lab/pdl-api/issues/270)

### Changed
- Change house api path. [#295](https://github.com/policy-design-lab/pdl-api/issues/295)
- Add feature to specify running port. [285](https://github.com/policy-design-lab/pdl-api/issues/285)

### Fixed
- Fix calculation error in house outlay JSON data file. [#306](https://github.com/policy-design-lab/pdl-api/issues/306)

## [0.21.0] - 2024-12-10

### Added
- Add house outlay to Title II endpoint. [#280](https://github.com/policy-design-lab/pdl-api/issues/280)
- Add practice names to house outlay api. [#288](https://github.com/policy-design-lab/pdl-api/issues/288)

### Changed
- Switch to using | (pipe) as delimiter for query parameters in EQP and CSP state distribution endpoints. [#286](https://github.com/policy-design-lab/pdl-api/issues/286)

## [0.20.0] - 2024-11-25

### Added
- Endpoints to get practice codes and names for EQIP and CSP. [#263](https://github.com/policy-design-lab/pdl-api/issues/263)
- Total payment grouped by practice codes to state distribution endpoint for EQIP and CSP, with query parameter support. [#275](https://github.com/policy-design-lab/pdl-api/issues/275)

### Fixed
- SNAP average monthly participation and percentage calculation across years. [#278](https://github.com/policy-design-lab/pdl-api/issues/278)

## [0.19.0] - 2024-11-03

### Changed
- Landing page values to use data from the database. [#258](https://github.com/policy-design-lab/pdl-api/issues/258)

### Fixed
- Title-II total payment calculation and overall benefits payment amounts calculation in the GET /pdl/allprograms endpoint. [#268](https://github.com/policy-design-lab/pdl-api/issues/268) 

## [0.18.0] - 2024-10-07

### Changed
- Crop Insurance endpoints to use data from the database. [#241](https://github.com/policy-design-lab/pdl-api/issues/241)
- CRP endpoints to use data from the database. [#237](https://github.com/policy-design-lab/pdl-api/issues/237)
- ACEP endpoints to use data from the database. [#239](https://github.com/policy-design-lab/pdl-api/issues/239)
- RCPP endpoints to use data from the database. [#241](https://github.com/policy-design-lab/pdl-api/issues/241)
- ProgramName attribute has been removed from crop insurance's state-distibution output [#255](https://github.com/polciy-design-lab/pdl-api/issues/255)

## [0.17.0] - 2024-08-28

### Added
- CSP IRA endpoints including state distribution and summary. [#234](https://github.com/policy-design-lab/pdl-api/issues/234)

### Changed
- Endpoints by removing hardcoded program and subtitle IDs. [#232](https://github.com/policy-design-lab/pdl-api/issues/232)

## [0.16.0] - 2024-08-16

### Changed
- EQIP and CSP endpoints to use data from the database. [#203](https://github.com/policy-design-lab/pdl-api/issues/203)

### Fixed
- Error when calling GET states endpoint after recent change. [#228](https://github.com/policy-design-lab/pdl-api/issues/228)
- Error due to the previous SNAP program ID being used. [#230](https://github.com/policy-design-lab/pdl-api/issues/230)
- Missing attributes in CSP response statute objects. [#232](https://github.com/policy-design-lab/pdl-api/issues/232) 

## [0.15.0] - 2024-07-19

### Added
- Issue templates. [#220](https://github.com/policy-design-lab/pdl-api/issues/220)

### Changed
- EQIP IRA's practice name list for the future got aggregated. [#218](https://github.com/polciy-design-lab/pdl-api/issues/218)
- EQIP IRA summary and state distribution JSON data. [#222](https://github.com/polciy-design-lab/pdl-api/issues/222)

## [0.14.0] - 2024-07-03

### Changed
- Update Title-4 endpoints to use database calls. [#190](https://github.com/policy-design-lab/pdl-api/issues/190)
- Update EQIP IRA data with changed name of US Virgin Islands. [#201](https://github.com/policy-design-lab/pdl-api/issues/201)
- Update EQIP IRA state distribution data [#205](https://githoub.com/policy-design-lab/pdl-api/issues/205)
- Update EQIP IRA summary data with future predctions. [#207](https://github.com/policy-design-lab/pdl-api/issues/207)
- Update EQIP IRA state distribution data [#208](https://github.com/policy-design-lab/pdl-api/issues/208)
- EQIP IRA state distribution's nationwide data matches with summary [#210](https://github.com/policy-design-lab/pdl-api/issues/210)
- EQIP IRA to use only 50 U.S. state data [#212](https://github.com/policy-design-lab/pdl-api/issues/212)
- EQIP IRA's budget authority data updated [#214](https://github.com/polciy-design-lab/pdl-api/issues/214)

### Added
- Endpoints for Title I's state distribution and summary. [#193](https://github.com/policy-design-lab/pdl-api/issues/193)
- EQIP IRA endpoint for state distribution [#195](https://github.com/policy-design-lab/pdl-api/issues/195)
- EQIP IRA endpoint for practice categories [#200](https://github.com/policy-design-lab/pdl-api/issues/200)
- EQIP IRA endpoint for aggregated prediction data [#204](https://github.com/policy-design-lab/pdl-api/issues/204)

## [0.13.0] - 2024-06-03

### Changed
- Update Title-1 endpoints to use database calls. [#182](https://github.com/policy-design-lab/pdl-api/issues/182) 
- All programs and summary JSON files based on already mapped data. [#188](https://github.com/policy-design-lab/pdl-api/issues/179)

## [0.12.0] - 2024-04-09

### Removed
- Retired old endpoints. [#179](https://github.com/policy-design-lab/pdl-api/issues/179)

## [0.11.0] - 2024-02-22

### Changed
- Update EQIP and CSP state distribution JSON files. [#170](https://github.com/policy-design-lab/pdl-api/issues/170)
- Renamed Pastured Cropland to Grassland in CSP JSON files. [#172](https://github.com/policy-design-lab/pdl-api/issues/172)

## [0.10.0] - 2024-02-09

### Added
- Summary endpoint for Title 1 and Title 2. [#163](https://github.com/policy-design-lab/pdl-api/issues/163)
- Title XI endpoints for crop insurance data. [#165](https://github.com/policy-design-lab/pdl-api/issues/165)
- Title IV endpoints for SNAP data. [#166](https://github.com/policy-design-lab/pdl-api/issues/166)

### Changed
- Update the API to use the renamed json files. [#162](https://github.com/policy-design-lab/pdl-api/issues/162)

## [0.9.0] - 2024-02-02

### Changed
- API Endpoints changed for Title I and Title II. [#155](https://github.com/policy-design-lab/pdl-api/issues/155)
- Subtitle A JSON files updated to match with other subtitle JSON files. [#157](https://github.com/policy-design-lab/pdl-api/issues/157)
  
## [0.8.0] - 2023-11-09

### Added
- Title Commodities DMC and SADA endpoints. [#147](https://github.com/policy-design-lab/pdl-api/issues/147)

## [0.7.0] - 2023-10-18

### Added
- Title 2 Conservation ACEP endpoints. [#131](https://github.com/policy-design-lab/pdl-api/issues/131)
- Title 2 Conservation RCPP endpoints. [#133](https://github.com/policy-design-lab/pdl-api/issues/133)

## [0.6.1] - 2023-09-18

### Changed
- Title 2 Conservation CRP data updated [#125](https://github.com/policy-design-lab/pdl-api/issues/125)

## [0.6.0] - 2023-09-06 

### Added
- Title 2 Conservation CRP endpoints. [#79](https://github.com/policy-design-lab/pdl-api/issues/79)

### Changed
- Crop Insurance JSON files to include average area insured and use latest data. [#120](https://github.com/policy-design-lab/pdl-api/issues/120)

## [0.5.0] - 2023-08-22

### Added
- Crop Insurance endpoints. [#78](https://github.com/policy-design-lab/pdl-api/issues/78)

### Changed
- EQIP data based on latest information. [#97](https://github.com/policy-design-lab/pdl-api/issues/97)
- Title 1 Commodities JSON files. [#99](https://github.com/policy-design-lab/pdl-api/issues/99)
- Title 1 Commodities JSON files after raw data update. [#110](https://github.com/policy-design-lab/pdl-api/issues/110)
- Crop Insurance JSON files to use average liabilities. [#117](https://github.com/policy-design-lab/pdl-api/issues/117)
- All Programs and Summary JSON after updates to Title-1 data. [#115](https://github.com/policy-design-lab/pdl-api/issues/115)

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
- Open API specification file. [#50](https://github.com/policy-design-lab/pdl-api/issues/50)

[0.22.0]: https://github.com/policy-design-lab/pdl-api/compare/0.21.0...0.22.0
[0.21.0]: https://github.com/policy-design-lab/pdl-api/compare/0.20.0...0.21.0
[0.20.0]: https://github.com/policy-design-lab/pdl-api/compare/0.19.0...0.20.0
[0.19.0]: https://github.com/policy-design-lab/pdl-api/compare/0.18.0...0.19.0
[0.18.0]: https://github.com/policy-design-lab/pdl-api/compare/0.17.0...0.18.0
[0.17.0]: https://github.com/policy-design-lab/pdl-api/compare/0.16.0...0.17.0
[0.16.0]: https://github.com/policy-design-lab/pdl-api/compare/0.15.0...0.16.0
[0.15.0]: https://github.com/policy-design-lab/pdl-api/compare/0.14.0...0.15.0
[0.14.0]: https://github.com/policy-design-lab/pdl-api/compare/0.13.0...0.14.0
[0.13.0]: https://github.com/policy-design-lab/pdl-api/compare/0.12.0...0.13.0
[0.12.0]: https://github.com/policy-design-lab/pdl-api/compare/0.11.0...0.12.0
[0.11.0]: https://github.com/policy-design-lab/pdl-api/compare/0.10.0...0.11.0
[0.10.0]: https://github.com/policy-design-lab/pdl-api/compare/0.9.0...0.10.0
[0.9.0]: https://github.com/policy-design-lab/pdl-api/compare/0.8.0...0.9.0
[0.8.0]: https://github.com/policy-design-lab/pdl-api/compare/0.7.0...0.8.0
[0.7.0]: https://github.com/policy-design-lab/pdl-api/compare/0.6.1...0.7.0
[0.6.1]: https://github.com/policy-design-lab/pdl-api/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/policy-design-lab/pdl-api/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/policy-design-lab/pdl-api/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/policy-design-lab/pdl-api/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/policy-design-lab/pdl-api/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/policy-design-lab/pdl-api/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/policy-design-lab/pdl-api/releases/tag/0.1.0

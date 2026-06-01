# Reference Library Import Protocol

Status: ACTIVE
Priority: REQUIRED BEFORE WRITING
Project: The Academy of Curiosities / 学堂趣事录

## Purpose

This file defines how the local reference library should be imported into the project writing standards.

Target local folder named by creator:
D:/【AI Project】/【The Academy of Curiosities】/09_日本参考资料库

The assistant cannot directly read a local Windows folder unless the files are uploaded, zipped, or synchronized into this GitHub repository. After the files are provided, every reference must be converted into structured project standards.

## Import rule

No reference file should remain only as raw material. Every useful fact must be mapped into one of the project standard documents below.

## Required output documents

1. docs/world_reference/00_MASTER_REFERENCE_INDEX.md
   - list all imported files
   - source type
   - date or version
   - reliability rating
   - which writing module uses it

2. docs/world_reference/01_JAPAN_CAMPUS_CULTURE_STANDARD.md
   - school systems
   - classroom routines
   - school buildings and spatial routes
   - school lunch
   - cleaning duty
   - club, committee, and class-role activities
   - speech etiquette and peer rules

3. docs/world_reference/02_GEO_CLIMATE_LIGHT_STANDARD.md
   - latitude and longitude
   - altitude
   - topography
   - sunrise and sunset
   - day length
   - solar angle and classroom light
   - seasonal shadows
   - temperature
   - humidity
   - wind
   - rain, snow, typhoon, rainy season

4. docs/world_reference/03_WATER_TIDE_WEATHER_STANDARD.md
   - rivers
   - drainage
   - puddles
   - condensation
   - classroom humidity
   - coastal tides when relevant
   - sea breeze and land breeze
   - weather evidence rules for mystery plots

5. docs/world_reference/04_FOOD_DAILY_LIFE_STANDARD.md
   - school lunch
   - snacks
   - home breakfast and dinner clues
   - seasonal food
   - convenience store references
   - allergies and child safety limits

6. docs/world_reference/05_FLORA_FAUNA_PHENOLOGY_STANDARD.md
   - cherry blossom timing
   - plum blossom
   - hydrangea
   - cicadas
   - fallen leaves
   - pollen
   - seasonal insects
   - schoolyard plants
   - evidence rules based on flowering, smell, pollen, leaves, and insects

7. docs/world_reference/06_LANGUAGE_PUNS_SOUND_STANDARD.md
   - Japanese child speech
   - school vocabulary
   - honorifics
   - sound symbolism
   - homophones
   - pun safety rules
   - words that cannot be directly translated from Chinese

8. docs/world_reference/07_MYSTERY_FAIR_PLAY_EVIDENCE_STANDARD.md
   - fair-play detective rules
   - evidence visibility
   - science repeatability
   - child-verifiable experiments
   - forbidden coincidence
   - forbidden culture mistake
   - red-herring rules

9. docs/world_reference/08_SOURCE_RELIABILITY_RULES.md
   - primary source first
   - official local data first
   - weather and tide data must include place and date
   - no invented numerical values
   - uncertain facts must be tagged NEEDS_VERIFICATION

## Fact tagging system

Each imported fact must use one of these tags:

- VERIFIED_SOURCE: confirmed by reliable source
- CONSULTANT_CONFIRMED: approved by Japan Cultural Calibration Agent or human consultant
- LOCAL_VARIATION: varies by region or school
- SEASONAL_VARIATION: varies by month or season
- NEEDS_VERIFICATION: may be useful but cannot be used in final draft yet
- DO_NOT_USE: culturally wrong, scientifically unsafe, or not suitable for the IP

## Mystery writing hard rule

Any clue based on light, weather, shadow, tide, smell, flowering, school routine, food, language, or behavior must be scientifically and culturally checkable.

A mystery clue is not allowed unless the reference standard states:

- where it happens
- when it happens
- why it is possible
- how a child can observe it
- how the final explanation can be verified

## Required import workflow

1. Upload or sync the reference folder.
2. Generate file inventory.
3. Classify every file into modules.
4. Extract usable facts.
5. Tag every fact using the fact tagging system.
6. Merge facts into the standard documents.
7. Mark uncertain or regional facts.
8. Run Japan Cultural Calibration Agent review.
9. Run science and fair-play review.
10. Only then allow use in story drafts.

## Current status

**FIRST_PASS_COMPLETE** (2026-06-02)

The local folder `09_日本参考资料库/` (24 files) is synchronized in this repository. Facts have been extracted into:

- `docs/world_reference/00_MASTER_REFERENCE_INDEX.md` — master map + scene card + clue lookup
- `docs/world_reference/01`–`07` — writing standards by domain
- `docs/world_reference/08_SOURCE_RELIABILITY_RULES.md` — fact tagging

**Parallel L1 (Chinese workspace):** `02_创作原则与世界观/名古屋写作硬指标_本格科学参考.md`

### Next maintenance passes

1. Tag remaining facts from 09_ with `08` reliability levels where not yet tagged inline
2. Mark `NEEDS_VERIFICATION` items for Japan consultant review
3. Build per-volume clue index (Vol 1–10) in `00_MASTER_REFERENCE_INDEX.md` §6
4. Keep L1 hard metrics and world_reference in sync — no drift

### Upload note

ZIP upload is **not required** if `09_日本参考资料库/` is already in the repo. New materials: add to `09_/`, then run the import workflow §Required import workflow.

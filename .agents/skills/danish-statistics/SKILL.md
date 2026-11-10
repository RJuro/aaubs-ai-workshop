---
name: danish-statistics
description: Get numbers from Statistics Denmark (StatBank) and put them on a map of the municipalities. Use when the user asks about Danish regions, municipalities, population, education, income, firms or anything Statistics Denmark publishes.
---

# Statistics Denmark and maps

What you cannot know without being told:

- **The API** is open, no key: `https://api.statbank.dk/v1`. `/tables?search=<words>&lang=en` finds tables, `/tableinfo?id=<TABLE>&lang=en` lists the variables and their codes, `/data` returns numbers (POST JSON with `table`, `format: "CSV"`, `variables: [{"code": ..., "values": [...]}]`; add `"valuePresentation": "CodeAndValue"` to get codes as well as names).
- **Municipality borders** with the official codes (`lau_1`): `https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson`. Plot the polygons with matplotlib; no GIS packages needed. Coordinates may have a third value: use the first two.
- **Codes beat names.** There are 98 municipalities; StatBank also has regions, "all Denmark" and Christiansø. Join on the three-digit code, never on the name (Århus/Aarhus, Høje-Taastrup/Høje Taastrup).
- **Tables that are usually right** (check with `/tableinfo`, take the latest year):
  - education by municipality: `HFUDD11` (`BOPOMR` municipality, `HFUDD`: `H70` master's, `H80` PhD, `TOT`; `ALDER` age groups; `KØN`, `HERKOMST` → `TOT`)
  - population: `FOLK1A` (`OMRÅDE`, `KØN`, `ALDER`, `CIVILSTAND`, quarterly `Tid`)
  - income: `INDKP101` (average income by municipality)
  Search only if none of these fits.
- Save every download in `cache/` so the run gives the same result next year.

How you do it is up to you. Before you report: every municipality matched between data and map (say which did not), the national total or a known number checks against the source, and you have opened the map and looked at it.

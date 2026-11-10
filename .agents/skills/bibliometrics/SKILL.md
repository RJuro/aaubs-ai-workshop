---
name: bibliometrics
description: Describe a research field from a Web of Science or Scopus export - publications over time, journals, most cited works, and the topics in the abstracts. Use when the user gives a WoS/Scopus export or asks what a field looks like.
---

# Bibliometrics from an export

What you cannot know without being told:

- **WoS plain-text format:** one field per line with a two-letter tag (`TI` title, `AU` authors, `PY` year, `SO` journal, `DE` keywords, `AB` abstract, `TC` times cited, `CR` cited references). Continuation lines start with three spaces; `ER` ends a record. A short parser is enough.
- **Topics:** embed the abstracts with `embed()` from `steps/llm.py` (mistral-embed), reduce and cluster (UMAP + HDBSCAN if installed, otherwise k-means on the vectors is fine), then let the model name each cluster from its most typical titles. Show the names with counts and a 2D map.
- Counts by year are distorted at the edges (the current year is incomplete): say so.

Choose the method that fits the data. Before you report: the number of records parsed matches the export, a few counts checked by hand, each topic name fits its titles (show three titles per topic).

WoS exports are licensed to AAU: do not share them outside.

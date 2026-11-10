# 07 What does a field look like?

**Input:** your own export: Web of Science ("Export → Plain text file", full record with cited references, up to 500 records) or Scopus (CSV). Put it in `input/`. Exports are licensed to AAU: do not share them.

**Prompt:**
> Work in `workflows/07-bibliometrics`. What does this field look like? Publications over time, main journals, most cited works, and the main topics.

**Skills it reads:** `notebook`, `bibliometrics`. Topic maps need `pip install umap-learn scikit-learn` (the agent asks).

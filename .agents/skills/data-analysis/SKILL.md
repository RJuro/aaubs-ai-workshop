---
name: data-analysis
description: Analyse a dataset (CSV, Excel, Stata, survey export) with a question - describe, plot, model, check - in Python or R, as a notebook run. Use when the user gives data and asks for descriptives, plots, regressions or a robustness check.
---

Work as in the `notebook` skill. If unclear, ask once: the question, the unit of observation, Python or R, and whether the data contain personal information (then only code and summaries go to a model, never the data).

Order: describe the data (rows, units, missing values) → plot the relation the question is about → model, simple first, then add controls → look at the cases the model fits worst. Use standard errors that fit the data (clustered for panels, robust otherwise).

Write effect sizes in plain words, say what is correlation, and open every figure before showing it.


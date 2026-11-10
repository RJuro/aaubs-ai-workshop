# 05 Two messy files from a colleague

**Input:** `input/kommune_indkomst.csv` (average disposable income per person 2024 and change from 2023, Danish municipality names, no codes) and `input/uddannelse_og_befolkning.xlsx` (code, name, population 1 Jan 2025, share of 30-64-year-olds with a master's or PhD). Put together by hand, nobody has checked them. (Made from public Statistics Denmark data, with problems planted on purpose.)

**Prompt:**
> Work in `workflows/05-messy-merge`. My colleague sent me these two files. Do municipalities with more highly educated people have higher incomes? Keep a log of every problem you fix.

**Skills it reads:** `notebook`, `data-analysis`.

**Watch for:** one typo changes the answer completely. Did the agent find it?

# Notes for a short paper (Roman, 10 Nov)

Working title: Where the graduates live. Education and income across Danish municipalities

Format: a short note, 4 to 5 pages, for the department working paper series. Plain language, readers are colleagues in economics and management, not regional economists.

## Question
- Do municipalities with more people holding a master's degree or PhD have higher average incomes?
- How strong is it, and which municipalities do not fit?

## Data
- `municipalities_2024.csv`: the 98 municipalities. Average disposable income per person 2024 and 2023 (DKK), population 1 Jan 2025, share of 30-64-year-olds with a master's degree or PhD in 2025 (%). Source: Statistics Denmark (tables INDKP and HFUDD).

## What I want in it
- Intro: the agglomeration and human capital story in one paragraph (Glaeser and Maré on cities and skills, Moretti on the new geography of jobs). Why it matters for Danish regional policy: the debate about moving education and state jobs out of Copenhagen.
- Data section: short, with a table of descriptives.
- Results: one scatter plot (education share vs income, log scale for income is fine), one simple regression (income on education share, maybe with log population as control). Report the slope in plain words: what one percentage point more graduates is associated with.
- The outliers: name the five municipalities furthest from the line and say something sensible about why (commuter suburbs, islands, wealthy north of Copenhagen).
- Discussion: correlation, not causation. Sorting vs spillovers (Moretti 2004). Where people live, not where they work.
- Conclusion: three or four sentences.

## Style
- My usual setup: `main.tex` as the spine, `preamble.tex`, one file per section in `sections/`, `references.bib`, build with `latexmk -pdf main`.
- No em-dashes. Short sentences. No "delve", no "crucial", no "landscape".
- Cite only what is in `references.bib`. If something needs a source that is not there, put `\needcite`.

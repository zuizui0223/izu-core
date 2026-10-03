# Chapter 2 empirical-emulation negative audit — 2026-10-03

## Decision

The Chapter 2 empirical-emulation sequence is **stopped**.

Four prospectively frozen attempts asked whether a Model 3-derived numerical world
could quantitatively reproduce the Chapter 1 H1-H4 empirical pattern. None
established the full target. The failures are retained as evidence for the existing
scope boundary rather than used to motivate indefinite model expansion.

This audit does not replace the established Chapter 2 result. It clarifies what
that result is **not**:

> Model 3 reconstructs a mechanistically compatible island-syndrome structure, but
> it does not quantitatively reproduce the Chapter 1 macroecological coefficient
> vector.

## Attempt 1 — Model3R-v1

**Prospective search:** 64 parameter draws.  
**Passes:** 0.

The best candidate reproduced the positive H3 isolation-to-pollen-limitation
gradient closely, but generalized accessibility did not increase with isolation
across all four contexts and the H4 assurance-to-pollen-limitation association
had the wrong sign.

The v1 decision was prospectively frozen as: do not widen the same parameter
search.

## Attempt 2 — Model3R-v2

**Prospective search:** 64 draws using real island covariates, four lineages per
island and distance/climate-dependent visitor assembly.  
**Passes:** 0.

H3 was again reproduced closely and the isolation-driven assurance response became
more realistic. The remaining mismatch was structural: generalized accessibility
was negative with isolation in all four contexts in the best draw, and H4
assurance still had the wrong sign.

The v2 decision was prospectively frozen as: do not widen the same v2 search.

## Attempt 3 — Model3R-v3 assembly-first

**Prospective search:** 96 draws with a source-species pool and assembly filtering.  
**Passes:** 0.

This revision made real progress. The best draw reproduced H3 and recovered the
empirical negative H4 associations of both assurance and generalization with
current pollen limitation. But it still failed the regional H2 isolation pattern:
the island-flora composition did not become enriched in assurance and generalized
accessibility with isolation in the observed way.

The v3 decision was to stop adding mechanisms and diagnose the assembly filter.

## Attempt 4 — Model3E-v1

Model3E separated fitting from validation.

**Training:** H1 domain slopes plus H3.  
**Held out:** H2 and H4.

Forty-eight parameter sets were screened; 13 met the preregistered eligibility
rule and five were frozen before held-out outcomes were opened.

The training stage already showed a major failure: the display-dulling domain was
not reproduced; all five accepted sets had display NRMSE = 1 with optimal display
scale 0.

The held-out result was then:

- frozen accepted sets: 5;
- successful H2/H4 sets: **0/5**.

The best H1/H3 set reproduced positive selfing-adjusted accessibility in three of
four regions but failed the southern-extratropical direction, and its H4 assurance
coefficient had the wrong sign.

## What the sequence means

The sequence is not four independent tests of one fixed model. The model family
changed after each failure:

```text
single-population response
  -> empirical covariates + multiple lineages
  -> assembly-first species filtering
  -> alternate Model3E focal-population formulation
```

Therefore it would be misleading to pool the searches into one numerical failure
rate. The important fact is the **model-selection history**: every revision was
frozen prospectively, but the next model structure was chosen after seeing the
previous failure.

Continuing with a fifth or sixth Chapter 2 emulator until one passed would turn
the exercise into open-ended model-space search. A later passing model would then
be a survivor of the exploratory sequence even if its own final run were
preregistered.

## Scientific conclusion

These negative results strengthen the already established scope boundary.

They show that the current Chapter 2 mechanism can reproduce:

- recurrent coarse functional response;
- state-dependent selection;
- reproductive buffering/persistence;
- genetic-accessibility and finite-realization effects;

without establishing a quantitative reconstruction of the Chapter 1 regional
coefficients.

That distinction is scientifically useful. Chapter 1 measures the macroecological
flora-level pattern. Chapter 2 provides a mechanistic numerical reconstruction of
how such a pattern can be generated in principle. It does not fit the four Chapter
1 regions or reproduce their exact coefficient vector.

## Future flora-level model

A multi-species flora-assembly model remains a legitimate future project because
Chapter 1's observational unit is an island flora rather than one evolving focal
population.

But that project is **not a Chapter 2 completion task**. If pursued, it should:

1. explicitly cite this four-model failure history;
2. freeze the model family before opening new validation outcomes;
3. separate fitting and held-out validation;
4. avoid using success as a requirement for retaining the established Chapter 2
   mechanistic result.

## Repository disposition

- PR #386 is closed without merge.
- The exploratory Model3E implementation from historical PR #387 is removed from
  the active Chapter 2 surface.
- Git history preserves the full implementations and frozen results.
- This audit is the only Chapter 2 mainline representation of the empirical
  emulation sequence.

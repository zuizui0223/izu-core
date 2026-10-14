# Approved investment variation probe

Spec: docs/CHAPTER2_INVESTMENT_VARIATION_RESTORATION_PROTOCOL_20261013.md

1. Freeze protocol and add failing tests for mean-preserving I-only restoration,
   boundary rejection, extinction primary handling and retained no-trigger pairs.
2. Implement minimal source-bound replay/continuation adapter; do not edit biology.
3. Admit all 64 original histories before launch; save replay receipt.
4. Run exactly 64 paired continuations, independently inspect raw records, summarize
   the frozen primary and descriptive outputs without retuning.
5. Review the whole change, integrate only supported interpretation into the four
   questions, publish reviewable source/results on the existing PR branch.

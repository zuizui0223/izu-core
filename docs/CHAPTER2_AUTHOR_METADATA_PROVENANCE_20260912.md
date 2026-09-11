# Chapter 2 author-metadata provenance

Updated: 2026-09-12

## Purpose

This file records identity fields that are already supported by an external source-locked repository record. It does **not** freeze final authorship, author order, corresponding-author status, ORCID, funding, acknowledgements, conflict declarations or submission declarations.

## Verified reusable identity fields

Source: `zuizui0223/fcp`, commit `8144856db9525ec40a6f910db22037ce24300a5d`, file `docs/jbi_author_confirmation_form.md`.

That source explicitly marks the following as already supported by author-provided, university-linked or official institutional records:

- full name: **ZHANG RUIQI**;
- division: **Division of Forest and Biomaterials Science**;
- institutional affiliation: **Graduate School of Agriculture, Kyoto University**;
- institutional postal address: **Kitashirakawa Oiwake-cho, Sakyo-ku, Kyoto 606-8502, Japan**;
- institutional email: **zhang.ruiqi.77h@st.kyoto-u.ac.jp**;
- current status in that source record: **research student**.

Recommended journal affiliation line if ZHANG RUIQI is confirmed as an author:

> Division of Forest and Biomaterials Science, Graduate School of Agriculture, Kyoto University, Kitashirakawa Oiwake-cho, Sakyo-ku, Kyoto 606-8502, Japan.

## Still unverified for this paper

The same source explicitly leaves these unresolved, so `izu-core` must remain fail-closed on them:

- final author order;
- whether there are additional coauthors;
- corresponding-author designation;
- ORCID;
- author approval;
- acknowledgements;
- funding;
- conflict-of-interest statement;
- significance prior-work context;
- inclusion/EDI statement;
- ethics confirmation;
- explicit submission declarations.

No ORCID was verified in the source record. Do not invent one or infer it from name/email matching.

## Routing rule

The verified identity fields above may be prefilled only after the user confirms that ZHANG RUIQI is part of the final author list for this Chapter 2 paper. Prefill must not be interpreted as confirmation of sole authorship, first authorship or corresponding-author status.

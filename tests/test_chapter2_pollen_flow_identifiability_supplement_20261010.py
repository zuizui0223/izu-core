"""Self-contained exact arithmetic checks of the concise manuscript appendix.

No source simulation, no ecological samples, no historical claims.
"""
from fractions import Fraction as Q
from math import exp
from pathlib import Path

A = (
    (Q(0), Q(1,2), Q(1,2)),
    (Q(1,2), Q(0), Q(1,2)),
    (Q(1,2), Q(1,2), Q(0)),
)
B = (
    (Q(0), Q(9,10), Q(9,10)),
    (Q(1,10), Q(0), Q(1,10)),
    (Q(9,10), Q(1,10), Q(0)),
)
ROOT = Path(__file__).resolve().parents[1]


def incoming(matrix):
    return tuple(sum((matrix[i][j] for i in range(3)), Q(0))
                 for j in range(3))


def paternal(matrix):
    return tuple(sum(row, Q(0)) for row in matrix)


def test_rational_witness_has_identical_recipient_pollen_and_different_donors():
    assert incoming(A) == incoming(B) == (Q(1), Q(1), Q(1))
    assert paternal(A) == (Q(1), Q(1), Q(1))
    assert paternal(B) == (Q(9,5), Q(1,5), Q(1))
    assert sum(incoming(A)) == sum(incoming(B)) == 3
    share_a = tuple(v / 3 for v in paternal(A))
    share_b = tuple(v / 3 for v in paternal(B))
    assert share_a == (Q(1,3), Q(1,3), Q(1,3))
    assert share_b == (Q(3,5), Q(1,15), Q(1,3))
    assert sum(abs(a-b) for a,b in zip(share_a, share_b)) == Q(8,15)


def test_recipient_concavity_gives_sharp_fixed_total_bounds():
    n, D, O, assurance, depression, pollen_scale = 3, 3., 4., .25, .2, 1.
    q = assurance * (1-depression)
    def g(r):
        return n*q*O + (1-q)*O * sum(
            1-exp(-x/(2*pollen_scale)) for x in r)
    lower = n*q*O + (1-q)*O*(1-exp(-D/(2*pollen_scale)))
    upper = n*q*O + (1-q)*O*n*(1-exp(-D/(2*n*pollen_scale)))
    assert abs(g((D,0,0)) - lower) < 1e-12
    assert abs(g((D/n,)*n) - upper) < 1e-12
    assert lower < upper


def test_family_has_opposite_father_credit_gradients_at_same_seed_state():
    H = Q(1,1000)
    difference = tuple(tuple(B[i][j] - A[i][j] for j in range(3))
                       for i in range(3))
    up = tuple(tuple(A[i][j] + H * difference[i][j] for j in range(3))
               for i in range(3))
    down = tuple(tuple(A[i][j] - H * difference[i][j] for j in range(3))
                 for i in range(3))
    assert incoming(up) == incoming(down) == incoming(A)
    assert paternal(up)[0] > paternal(A)[0] > paternal(down)[0]
    assert all(v >= 0 for matrix in (up,down) for row in matrix for v in row)


def test_manuscript_keeps_confirmation_separate_from_exploration():
    paper=(ROOT / "docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md").read_text()
    appendix=(ROOT / "docs/CHAPTER2_POLLEN_FLOW_IDENTIFIABILITY_SUPPLEMENT_20261010.md").read_text()
    assert "post-discovery" in paper.lower()
    assert "not part of the four-setting confirmation" in paper
    assert "not the paper's corrected rare-mutant invasion gradient" in appendix
    assert "not a new prospectively confirmed result" in appendix
    assert "n(n-2)" in appendix

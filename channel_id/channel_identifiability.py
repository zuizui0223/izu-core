"""Exact identifiability boundaries for declared ``W = F * E`` studies.

This module ports the reusable mathematical core from ``microdonta`` without
porting its old Campanula assumptions or legacy ABMs.  It is deliberately small:

N1
    Net performance alone cannot identify which positive multiplicative channel
    changed.  ``(aF, E)`` and ``(F, aE)`` generate the same ``W = aFE``.
N2
    Positive ``W`` plus one directly observed factor reconstructs the other.
N3
    A proxy ``X = qF`` identifies *relative* channel change when ``q`` is stable
    across compared regimes.
N4
    If the proxy conversion can drift, the same observed ``W`` and ``X`` are
    compatible with different latent channel changes.

The results are conditional on the declared factorisation, a common trait domain,
and the positive interior.  Structural zeroes and extinction states must be
handled separately; this module never divides through them silently.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Literal, Sequence


Channel = Literal["local", "establishment"]
ChannelConclusion = Literal[
    "local_only",
    "establishment_only",
    "mixed",
    "unchanged",
]


def _positive(values: Sequence[float], *, name: str) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if not result:
        raise ValueError(f"{name} must be nonempty")
    if any(value <= 0.0 for value in result):
        raise ValueError(f"{name} must be strictly positive")
    return result


def _same_length(**series: Sequence[float]) -> int:
    lengths = {len(values) for values in series.values()}
    if len(lengths) != 1:
        detail = ", ".join(f"{name}={len(values)}" for name, values in series.items())
        raise ValueError(f"series must share a length ({detail})")
    return next(iter(lengths))


def _ratio(after: Sequence[float], before: Sequence[float]) -> tuple[float, ...]:
    return tuple(a / b for a, b in zip(after, before))


def _classify(
    local_ratio: Sequence[float],
    establishment_ratio: Sequence[float],
    *,
    tolerance: float = 1e-10,
) -> ChannelConclusion:
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    local_changed = any(abs(value - 1.0) > tolerance for value in local_ratio)
    establishment_changed = any(
        abs(value - 1.0) > tolerance for value in establishment_ratio
    )
    if local_changed and not establishment_changed:
        return "local_only"
    if establishment_changed and not local_changed:
        return "establishment_only"
    if local_changed and establishment_changed:
        return "mixed"
    return "unchanged"


@dataclass(frozen=True)
class VitalRateState:
    """Positive local and establishment channels on one ordered trait domain."""

    trait: tuple[float, ...]
    local: tuple[float, ...]
    establishment: tuple[float, ...]

    def __post_init__(self) -> None:
        n = len(self.trait)
        if n == 0 or len(self.local) != n or len(self.establishment) != n:
            raise ValueError("trait, local, and establishment must share a nonzero length")
        if any(right <= left for left, right in zip(self.trait, self.trait[1:])):
            raise ValueError("trait values must be strictly increasing")
        if any(value <= 0 for value in self.local + self.establishment):
            raise ValueError("W=F*E theorem functions require the positive interior")

    @property
    def net(self) -> tuple[float, ...]:
        return tuple(f * e for f, e in zip(self.local, self.establishment))


@dataclass(frozen=True)
class ChannelSymmetryResult:
    """Two different channel interventions with observationally identical net W."""

    attenuation: tuple[float, ...]
    local_change: VitalRateState
    establishment_change: VitalRateState
    net_equal: bool


@dataclass(frozen=True)
class ChannelChangeRatios:
    """Relative before/after change in the two declared channels."""

    local_ratio: tuple[float, ...]
    establishment_ratio: tuple[float, ...]
    conclusion: ChannelConclusion


@dataclass(frozen=True)
class ProxyAmbiguityResult:
    """Two calibration histories producing the same observed W and proxy X."""

    stable_calibration: ChannelChangeRatios
    drifting_calibration: ChannelChangeRatios
    same_observed_data: bool


def construct_net_only_symmetry(
    baseline: VitalRateState,
    attenuation: Sequence[float],
    *,
    tolerance: float = 1e-12,
) -> ChannelSymmetryResult:
    """Construct theorem N1: distinct channel changes with the same net output."""

    a = _positive(attenuation, name="attenuation")
    if len(a) != len(baseline.trait):
        raise ValueError("attenuation must share the trait-domain length")

    local_change = VitalRateState(
        trait=baseline.trait,
        local=tuple(scale * value for scale, value in zip(a, baseline.local)),
        establishment=baseline.establishment,
    )
    establishment_change = VitalRateState(
        trait=baseline.trait,
        local=baseline.local,
        establishment=tuple(
            scale * value for scale, value in zip(a, baseline.establishment)
        ),
    )
    net_equal = all(
        isclose(left, right, rel_tol=tolerance, abs_tol=tolerance)
        for left, right in zip(local_change.net, establishment_change.net)
    )
    return ChannelSymmetryResult(
        attenuation=a,
        local_change=local_change,
        establishment_change=establishment_change,
        net_equal=net_equal,
    )


def reconstruct_from_net_and_factor(
    *,
    trait: Sequence[float],
    net: Sequence[float],
    observed_factor: Sequence[float],
    factor: Channel,
) -> VitalRateState:
    """Apply theorem N2: positive W plus one exact factor identifies both factors."""

    z = tuple(float(value) for value in trait)
    w = _positive(net, name="net")
    observed = _positive(observed_factor, name="observed_factor")
    _same_length(trait=z, net=w, observed_factor=observed)
    if any(right <= left for left, right in zip(z, z[1:])):
        raise ValueError("trait values must be strictly increasing")

    if factor == "local":
        local = observed
        establishment = tuple(total / local_value for total, local_value in zip(w, local))
    elif factor == "establishment":
        establishment = observed
        local = tuple(total / e for total, e in zip(w, establishment))
    else:
        raise ValueError(f"unknown factor: {factor!r}")
    return VitalRateState(z, local, establishment)


def identify_relative_change_from_stable_proxy(
    *,
    net_before: Sequence[float],
    net_after: Sequence[float],
    proxy_before: Sequence[float],
    proxy_after: Sequence[float],
    proxy_channel: Channel = "local",
    tolerance: float = 1e-10,
) -> ChannelChangeRatios:
    """Apply theorem N3 for a proxy with a stable positive conversion factor.

    For a local-channel proxy ``X_i=qF_i`` with the same q in both regimes,
    ``F1/F0 = X1/X0`` and ``E1/E0 = (W1/W0)/(F1/F0)``.  Absolute calibration of
    q is not required for *relative* channel change.
    """

    w0 = _positive(net_before, name="net_before")
    w1 = _positive(net_after, name="net_after")
    x0 = _positive(proxy_before, name="proxy_before")
    x1 = _positive(proxy_after, name="proxy_after")
    _same_length(net_before=w0, net_after=w1, proxy_before=x0, proxy_after=x1)

    net_ratio = _ratio(w1, w0)
    proxy_ratio = _ratio(x1, x0)
    if proxy_channel == "local":
        local_ratio = proxy_ratio
        establishment_ratio = tuple(
            net_change / local_change
            for net_change, local_change in zip(net_ratio, local_ratio)
        )
    elif proxy_channel == "establishment":
        establishment_ratio = proxy_ratio
        local_ratio = tuple(
            net_change / establishment_change
            for net_change, establishment_change in zip(net_ratio, establishment_ratio)
        )
    else:
        raise ValueError(f"unknown proxy_channel: {proxy_channel!r}")

    return ChannelChangeRatios(
        local_ratio=local_ratio,
        establishment_ratio=establishment_ratio,
        conclusion=_classify(local_ratio, establishment_ratio, tolerance=tolerance),
    )


def construct_proxy_calibration_ambiguity(
    *,
    net_before: Sequence[float],
    net_after: Sequence[float],
    proxy_before: Sequence[float],
    proxy_after: Sequence[float],
    baseline_calibration: Sequence[float],
    calibration_shift: Sequence[float],
    proxy_channel: Channel = "local",
    tolerance: float = 1e-10,
) -> ProxyAmbiguityResult:
    """Construct theorem N4: calibration drift restores non-identifiability.

    The two latent histories use identical observed ``W`` and ``X``.  Model A
    keeps q stable.  Model B changes q by ``calibration_shift`` after the regime
    transition.  Different latent channel ratios therefore remain compatible with
    the same observations whenever the shift differs from one.
    """

    w0 = _positive(net_before, name="net_before")
    w1 = _positive(net_after, name="net_after")
    x0 = _positive(proxy_before, name="proxy_before")
    x1 = _positive(proxy_after, name="proxy_after")
    q0 = _positive(baseline_calibration, name="baseline_calibration")
    shift = _positive(calibration_shift, name="calibration_shift")
    _same_length(
        net_before=w0,
        net_after=w1,
        proxy_before=x0,
        proxy_after=x1,
        baseline_calibration=q0,
        calibration_shift=shift,
    )

    stable = identify_relative_change_from_stable_proxy(
        net_before=w0,
        net_after=w1,
        proxy_before=x0,
        proxy_after=x1,
        proxy_channel=proxy_channel,
        tolerance=tolerance,
    )

    q1 = tuple(base * multiplier for base, multiplier in zip(q0, shift))
    if proxy_channel == "local":
        f0 = tuple(x / q for x, q in zip(x0, q0))
        f1 = tuple(x / q for x, q in zip(x1, q1))
        e0 = tuple(w / f for w, f in zip(w0, f0))
        e1 = tuple(w / f for w, f in zip(w1, f1))
    elif proxy_channel == "establishment":
        e0 = tuple(x / q for x, q in zip(x0, q0))
        e1 = tuple(x / q for x, q in zip(x1, q1))
        f0 = tuple(w / e for w, e in zip(w0, e0))
        f1 = tuple(w / e for w, e in zip(w1, e1))
    else:
        raise ValueError(f"unknown proxy_channel: {proxy_channel!r}")

    local_ratio = _ratio(f1, f0)
    establishment_ratio = _ratio(e1, e0)
    drifting = ChannelChangeRatios(
        local_ratio=local_ratio,
        establishment_ratio=establishment_ratio,
        conclusion=_classify(local_ratio, establishment_ratio, tolerance=tolerance),
    )
    return ProxyAmbiguityResult(
        stable_calibration=stable,
        drifting_calibration=drifting,
        same_observed_data=True,
    )

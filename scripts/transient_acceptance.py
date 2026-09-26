#!/usr/bin/env python3
"""Decide what a steady screening result may claim once transient evidence exists.

Written before any transient case is run, which is the only time these rules mean anything.
Three outcomes and no fourth: a steady trend may be supported over the cases actually tested,
it may be overturned, or the evidence may be too weak to say either. "No difference" is never
one of them, because an effect smaller than its own uncertainty is unresolved, not absent.

The envelope arithmetic is deliberately not a bound. Adding a numerical term, a clocking
spread and a model spread summarises the choices that were sampled. Interactions between them
and error shared by every model sampled both lie outside it, so it is reported as a sampled
summary and never as a worst case.
"""
from __future__ import annotations

SUPPORTED = "STEADY_TREND_SUPPORTED_OVER_TESTED_CASES"
OVERTURNED = "STEADY_TREND_OVERTURNED"
UNRESOLVED = "UNRESOLVED"
NOT_FROZEN = "TOLERANCE_NOT_FROZEN"


def sampled_envelope(u_num, clocking_spread, model_spread):
    """Summarise the sampled numerical, clocking and model choices. NOT a bound."""
    return {
        "value": u_num + clocking_spread + model_spread,
        "components": {"u_num": u_num, "clocking_spread": clocking_spread,
                       "model_spread": model_spread},
        "is_a_bound": False,
        "note": ("Sum over sampled choices only. It is not a worst case on physical model error "
                 "and not a confidence interval: interactions can exceed an additive "
                 "main-effect construction, and bias shared by every model sampled is invisible "
                 "to it."),
    }


def phase_sampling_converged(endpoint_by_positions, tolerance):
    """Has refining the phase sampling stopped moving the phase-averaged endpoint?

    `endpoint_by_positions` maps a number of positions over the declared interval to the
    phase-averaged endpoint. Four positions are an initial budget, not an acceptance theorem,
    so at least two refinement levels are required before convergence can be claimed.
    """
    levels = sorted(endpoint_by_positions)
    if len(levels) < 2:
        return {"converged": False, "reason": "a single sampling level demonstrates nothing"}
    finest, previous = levels[-1], levels[-2]
    change = abs(endpoint_by_positions[finest] - endpoint_by_positions[previous])
    return {"converged": change <= tolerance, "change": change, "tolerance": tolerance,
            "levels": levels,
            "reason": ("phase-averaged endpoint moved %.6g between %d and %d positions"
                       % (change, previous, finest))}


def disposition(steady_delta, transient_delta, uncertainty, tolerance=None,
                phase_converged=True, time_step_converged=True, averaging_converged=True):
    """Classify what may be claimed. `uncertainty` is the sampled envelope value.

    Signs matter: a transient result that reverses the sign of the difference overturns the
    steady trend regardless of how small either value is, provided the evidence is usable.
    """
    if tolerance is None:
        return {"outcome": NOT_FROZEN,
                "reason": ("no prospective numerical tolerance is registered, so no acceptance "
                           "decision may be made; choosing one after seeing the result is the "
                           "move this specification exists to prevent")}
    unconverged = [n for n, ok in (("phase sampling", phase_converged),
                                   ("time step", time_step_converged),
                                   ("averaging window", averaging_converged)) if not ok]
    if unconverged:
        return {"outcome": UNRESOLVED,
                "reason": "numerical evidence is not usable: %s not converged" % ", ".join(unconverged)}
    difference = abs(transient_delta - steady_delta)
    reversed_sign = (steady_delta * transient_delta) < 0
    if reversed_sign:
        return {"outcome": OVERTURNED, "difference": difference,
                "reason": "the transient result reverses the sign of the steady difference"}
    if difference > tolerance:
        return {"outcome": OVERTURNED, "difference": difference,
                "reason": ("the transient mean differs from the steady screening value by "
                           "%.6g, beyond the registered tolerance %.6g" % (difference, tolerance))}
    if abs(transient_delta) <= uncertainty:
        return {"outcome": UNRESOLVED, "difference": difference,
                "reason": ("the transient effect %.6g lies inside its own sampled uncertainty "
                           "%.6g; that is unresolved, not evidence of no effect"
                           % (abs(transient_delta), uncertainty))}
    return {"outcome": SUPPORTED, "difference": difference,
            "reason": ("the transient mean agrees with the steady screening value within the "
                       "registered tolerance, over the cases actually tested")}

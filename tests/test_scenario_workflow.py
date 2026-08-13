from channel_id.scenario_workflow import TraitSummary, fit_scenarios, run_scenario_workflow

def rows():
    out=[]
    for trait, vals in {"size":[10,8,6,4,2], "guide":[10,2,2,2,2]}.items():
        for order, value in enumerate(vals):
            out.append(TraitSummary(trait, str(order), order, 0 if order==0 else 1, float(value), 0.2, 20))
    return tuple(out)

def test_mixed_channels_prefer_combined_scenario():
    result=fit_scenarios(rows())
    assert result["selected_scenario"] == "cline_plus_step"
    assert result["delta_bic"]["cline_plus_step"] == 0

def test_recovery_audit_has_all_scenarios():
    result=run_scenario_workflow(rows(), replicates=20, seed=1)
    assert set(result["recovery_audit"]["selection_rates"]) == {"cline", "bombus_loss_step", "cline_plus_step"}

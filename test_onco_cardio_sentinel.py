import pytest
from onco_cardio_sentinel import CumulativeDoseTrackerAgent, TroponinKineticsAgent, MyocarditisRiskStratifierAgent, OncoCardioCoordinator, main  # noqa: E402


def test_sub_agents():
    a1 = CumulativeDoseTrackerAgent()
    alerts1 = a1.evaluate({"metric_primary": 35.0})
    assert len(alerts1) == 1

    a2 = TroponinKineticsAgent()
    alerts2 = a2.evaluate({"critical_flag": True})
    assert len(alerts2) == 1

    a3 = MyocarditisRiskStratifierAgent()
    alerts3 = a3.evaluate({"status_text": "DISCORDANT_FINDING"})
    assert len(alerts3) == 1


def test_coordinator():
    coord = OncoCardioCoordinator()
    dossier = coord.audit_case({"case_id": "TEST-100", "metric_primary": 10.0, "metric_secondary": 2.0})
    assert dossier["overall_status"] == "CONCORDANT_NORMAL"
    assert dossier["total_alerts"] == 0

    ans = coord.query_assistant("What are the guidelines?")
    assert "guidelines" in ans or "standards" in ans


def test_cli():
    assert main(["audit", "--case-id", "CLI-01"]) == 0
    assert main(["chat", "What", "is", "the", "system", "status?"]) == 0


def test_domain_registry():
    from onco_cardio_sentinel import DomainKnowledgeRegistry
    assert DomainKnowledgeRegistry.ZERO_PHI_COMPLIANCE is False
    assert "PRO" in DomainKnowledgeRegistry.SYSTEM_VERSION


def test_legacy_csv_false_flags_and_status_aliases(tmp_path):
    import csv
    from onco_cardio_sentinel import TroponinKineticsAgent, MyocarditisRiskStratifierAgent
    worker = TroponinKineticsAgent()
    assert worker.evaluate({"metric_secondary": "5", "critical_flag": "False"}) == []
    assert len(MyocarditisRiskStratifierAgent().evaluate({"status_flag": "DISCORDANT"})) == 1

    src = tmp_path / "example.csv"
    out = tmp_path / "output.csv"
    src.write_text(
        "case_id,metric_primary,metric_secondary,is_stat,status_flag\n"
        "C1,10,5,False,NORMAL\n"
        "C2,10,5,True,DISCORDANT\n",
        encoding="utf-8",
    )
    assert main(["batch", "--input", str(src), "--output", str(out)]) == 0
    with out.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 2
    assert rows[0]["critical_count"] == "0"
    assert rows[1]["critical_count"] == "1"

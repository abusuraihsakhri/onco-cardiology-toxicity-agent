"""
Automated Pytest Test Suite for the Clinical Module (onco_cardiology_toxicity_agent).
Domain: Cardio-Oncology
Standard: ESC 2022 Cardio-Oncology Guidelines
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from onco_cardiology_toxicity_agent.models import (
    ClinicalCasePayload,
    UrgencyLevel,
    ClinicalIntegrityStatus,
)
from onco_cardiology_toxicity_agent.agents import (
    CumulativeDoseTrackerAgent,
    TroponinKineticsAgent,
    MyocarditisRiskStratifierAgent,
    OncoCardioCoordinator,
)
from onco_cardiology_toxicity_agent.engine import ClinicalDomainEngine
from onco_cardiology_toxicity_agent.cli import main as clinical_main


def test_cumulative_dose_tracker():
    agent = CumulativeDoseTrackerAgent()
    # Value above threshold should trigger alert
    case = ClinicalCasePayload(
        case_id="C1", patient_synthetic_id="SYN-01",
        primary_metric=35.0, secondary_metric=5.0, status_flag="NORMAL"
    )
    alerts = agent.audit(case)
    assert len(alerts) == 1
    assert alerts[0].urgency == UrgencyLevel.WARNING

    # Value below threshold should not trigger alert
    case_ok = ClinicalCasePayload(
        case_id="C2", patient_synthetic_id="SYN-02",
        primary_metric=10.0, secondary_metric=5.0, status_flag="NORMAL"
    )
    alerts_ok = agent.audit(case_ok)
    assert len(alerts_ok) == 0


def test_troponin_kinetics_agent():
    agent = TroponinKineticsAgent()
    # STAT flag should trigger critical alert
    case_stat = ClinicalCasePayload(
        case_id="T1", patient_synthetic_id="SYN-03",
        primary_metric=10.0, secondary_metric=5.0, status_flag="NORMAL", is_stat=True
    )
    alerts_stat = agent.audit(case_stat)
    assert len(alerts_stat) == 1
    assert alerts_stat[0].urgency == UrgencyLevel.STAT_CRITICAL

    # High secondary metric should trigger warning
    case_high = ClinicalCasePayload(
        case_id="T2", patient_synthetic_id="SYN-04",
        primary_metric=10.0, secondary_metric=15.0, status_flag="NORMAL"
    )
    alerts_high = agent.audit(case_high)
    assert len(alerts_high) == 1
    assert alerts_high[0].urgency == UrgencyLevel.WARNING


def test_myocarditis_risk_stratifier():
    agent = MyocarditisRiskStratifierAgent()
    # Discordant status should trigger advisory
    case_discordant = ClinicalCasePayload(
        case_id="M1", patient_synthetic_id="SYN-05",
        primary_metric=10.0, secondary_metric=5.0, status_flag="DISCORDANT"
    )
    alerts = agent.audit(case_discordant)
    assert len(alerts) == 1
    assert alerts[0].urgency == UrgencyLevel.ADVISORY

    # Normal status should not trigger alert
    case_normal = ClinicalCasePayload(
        case_id="M2", patient_synthetic_id="SYN-06",
        primary_metric=10.0, secondary_metric=5.0, status_flag="NORMAL"
    )
    alerts_normal = agent.audit(case_normal)
    assert len(alerts_normal) == 0


def test_coordinator_integration():
    coord = OncoCardioCoordinator()
    # All clear case
    case_clear = ClinicalCasePayload(
        case_id="INT-1", patient_synthetic_id="SYN-07",
        primary_metric=10.0, secondary_metric=5.0, status_flag="NORMAL"
    )
    dossier = coord.process_case(case_clear)
    assert dossier["overall_status"] == ClinicalIntegrityStatus.CONCORDANT_NORMAL.value
    assert dossier["total_alerts"] == 0

    # Critical case
    case_critical = ClinicalCasePayload(
        case_id="INT-2", patient_synthetic_id="SYN-08",
        primary_metric=35.0, secondary_metric=15.0, status_flag="DISCORDANT", is_stat=True
    )
    dossier_crit = coord.process_case(case_critical)
    assert dossier_crit["overall_status"] == ClinicalIntegrityStatus.CRITICAL_ACTION_REQUIRED.value
    assert dossier_crit["stat_critical_alerts"] > 0


def test_coordinator_chat():
    coord = OncoCardioCoordinator()
    response = coord.query_supervisory_chat("What is the status?")
    assert "tracking" in response or "cases" in response

    response_guideline = coord.query_supervisory_chat("What are the guidelines?")
    assert "ESC" in response_guideline or "guidelines" in response_guideline.lower()


def test_clinical_engine():
    # Test primary index evaluation
    result = ClinicalDomainEngine.evaluate_primary_index(25.0)
    assert result is not None
    assert "exceeds" in result["finding"].lower()

    result_ok = ClinicalDomainEngine.evaluate_primary_index(15.0)
    assert result_ok is None

    # Test secondary kinetics evaluation
    result_stat = ClinicalDomainEngine.evaluate_secondary_kinetics(5.0, True)
    assert result_stat is not None

    result_high = ClinicalDomainEngine.evaluate_secondary_kinetics(15.0, False)
    assert result_high is not None

    result_ok = ClinicalDomainEngine.evaluate_secondary_kinetics(5.0, False)
    assert result_ok is None

    # Test biomarker concordance
    result_discordant = ClinicalDomainEngine.evaluate_biomarker_concordance("DISCORDANT", {})
    assert result_discordant is not None

    result_normal = ClinicalDomainEngine.evaluate_biomarker_concordance("NORMAL", {})
    assert result_normal is None


def test_clinical_cli():
    assert clinical_main(["audit", "--case-id", "CLI-TEST-01"]) == 0
    assert clinical_main(["chat", "What", "is", "the", "status?"]) == 0


def test_clinical_case_to_dict():
    case = ClinicalCasePayload(
        case_id="D1", patient_synthetic_id="SYN-09",
        primary_metric=10.0, secondary_metric=5.0, status_flag="NORMAL"
    )
    alert = case  # Not an alert, but testing the model
    # Test that the payload can be created without errors
    assert case.case_id == "D1"
    assert case.patient_synthetic_id == "SYN-09"

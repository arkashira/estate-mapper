import json
from estate_mapper import EstateMapper, Asset

def test_generate_report_decommissioning():
    assets = [
        Asset("VM1", "VM", 5),
        Asset("VM2", "VM", 60),
    ]
    estate_mapper = EstateMapper(assets)
    report = estate_mapper.generate_report("decommissioning")
    assert json.loads(report) == ["Decommission VM1 (VM)"]

def test_generate_report_migration():
    assets = [
        Asset("VM1", "VM", 5),
        Asset("VM2", "VM", 60),
    ]
    estate_mapper = EstateMapper(assets)
    report = estate_mapper.generate_report("migration")
    assert json.loads(report) == ["Migrate VM2 (VM)"]

def test_generate_report_consolidation():
    assets = [
        Asset("VM1", "VM", 5),
        Asset("VM2", "VM", 60),
    ]
    estate_mapper = EstateMapper(assets)
    report = estate_mapper.generate_report("consolidation")
    assert json.loads(report) == ["Consolidate VM1 (VM)"]

def test_rank_reports():
    assets = [
        Asset("VM1", "VM", 5),
        Asset("VM2", "VM", 60),
        Asset("Service1", "Service", 20),
        Asset("Service2", "Service", 80),
    ]
    estate_mapper = EstateMapper(assets)
    decommissioning_report = estate_mapper.generate_report("decommissioning")
    migration_report = estate_mapper.generate_report("migration")
    consolidation_report = estate_mapper.generate_report("consolidation")
    reports = [decommissioning_report, migration_report, consolidation_report]
    ranked_reports = estate_mapper.rank_reports(reports)
    assert len(ranked_reports) == 3

def test_invalid_scenario():
    assets = [
        Asset("VM1", "VM", 5),
    ]
    estate_mapper = EstateMapper(assets)
    try:
        estate_mapper.generate_report("invalid")
        assert False
    except ValueError:
        assert True

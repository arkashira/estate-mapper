import json
from dataclasses import dataclass
from typing import List

@dataclass
class Asset:
    name: str
    type: str
    usage: int

class EstateMapper:
    def __init__(self, assets: List[Asset]):
        self.assets = assets

    def generate_report(self, scenario: str) -> str:
        if scenario not in ["decommissioning", "migration", "consolidation"]:
            raise ValueError("Invalid scenario")
        report = []
        for asset in self.assets:
            if scenario == "decommissioning" and asset.usage < 10:
                report.append(f"Decommission {asset.name} ({asset.type})")
            elif scenario == "migration" and asset.usage > 50:
                report.append(f"Migrate {asset.name} ({asset.type})")
            elif scenario == "consolidation" and asset.usage < 50:
                report.append(f"Consolidate {asset.name} ({asset.type})")
        return json.dumps(report)

    def rank_reports(self, reports: List[str]) -> List[str]:
        ranked_reports = []
        for report in reports:
            ranked_reports.append((report, len(json.loads(report))))
        ranked_reports.sort(key=lambda x: x[1], reverse=True)
        return [report[0] for report in ranked_reports]

def main():
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
    print(ranked_reports)

if __name__ == "__main__":
    main()

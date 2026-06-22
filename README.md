# Estate Mapper
Estate Mapper is a tool for generating ranked reports for safe decommissioning and migration of assets.

## Usage
1. Create an instance of the `EstateMapper` class, passing in a list of `Asset` objects.
2. Call the `generate_report` method, passing in the desired scenario ("decommissioning", "migration", or "consolidation").
3. Call the `rank_reports` method, passing in a list of reports.

## Example

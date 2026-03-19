## ADDED Requirements

### Requirement: Simplified git stats output
The `archive_with_stats.py` script SHALL output simplified statistics without `branch` and `repository` fields in the CSV file.

#### Scenario: CSV output format
- **WHEN** the script executes successfully
- **THEN** the CSV header contains: id, author, timestamp, additions, deletions, changed_files, changed_functions, total_lines, project_name
- **THEN** the CSV data row excludes branch and repository columns

#### Scenario: Script execution
- **WHEN** the script runs
- **THEN** `get_current_branch()` is not called for statistics collection
- **THEN** `repository` field is not included in the returned stats object

## MODIFIED Requirements

## REMOVED Requirements

### Requirement: Repository field in stats
**Reason**: Repository name is derived from git root basename which adds unnecessary complexity
**Migration**: Not applicable - this field is removed from output

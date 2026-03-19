## ADDED Requirements

### Requirement: Auto-dependency-install functionality
The `xt-openspec-wrapper-init` script SHALL automatically check for and install required dependencies (openspec and openspec-cn) if they are not present on the system.

#### Scenario: Dependencies not installed
- **WHEN** user runs `xt-openspec-wrapper-init` and neither `openspec` nor `openspec-cn` is installed
- **THEN** system automatically runs `npm install -g @fission-ai/openspec@latest` and `npm install -g @studyzy/openspec-cn@latest`
- **AND** both installations complete successfully

#### Scenario: Partial dependencies installed
- **WHEN** user runs `xt-openspec-wrapper-init` and only `openspec` is installed
- **THEN** system automatically runs `npm install -g @studyzy/openspec-cn@latest` for the missing dependency
- **AND** the installation completes successfully

### Requirement: Auto-initialization
The `xt-openspec-wrapper-init` script SHALL run initialization commands for openspec tools if they are already installed.

#### Scenario: Dependencies already installed
- **WHEN** user runs `xt-openspec-wrapper-init` and both `openspec` and `openspec-cn` are already installed
- **THEN** system automatically runs `openspec init` with default configuration
- **AND** system automatically runs `openspec-cn init` with default configuration

### Requirement: Default tool configuration
The initialization commands SHALL configure for Cursor and Claude Code tools by default.

#### Scenario: Default tool selection
- **WHEN** `openspec init` and `openspec-cn init` are run
- **THEN** both tools (Cursor and Claude Code) are selected in the configuration
- **AND** no interactive prompts are required from the user

### Requirement: Error handling
If dependency installation or initialization fails, the script SHALL provide a friendly error message.

#### Scenario: Installation failure
- **WHEN** `npm install -g` command fails (e.g., due to permissions or network)
- **THEN** script displays a clear error message explaining the issue
- **AND** script suggests possible solutions (e.g., run with sudo, check network)

#### Scenario: Initialization failure
- **WHEN** `openspec init` or `openspec-cn init` fails
- **THEN** script displays a clear error message
- **AND** script informs user they can run the init commands manually

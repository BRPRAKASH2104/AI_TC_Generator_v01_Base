# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Installation and Setup
```bash
# Install dependencies
pip install -r ../utilities/requirements.txt

# Verify Python version (requires 3.13.5+)
python --version
```

### Running the Test Case Generator

**Primary command (latest version):**
```bash
python generate_contextual_tests_v002.py "../input/reqifz_files"
```

**With different models:**
```bash
python generate_contextual_tests_v002.py "../input/reqifz_files" --model deepseek-coder-v2:16b
python generate_contextual_tests_v002.py "../input/reqifz_files" --model llama3.1:8b
```

**With custom configuration:**
```bash
python generate_contextual_tests_v002.py "../input/reqifz_files" --config example_config.yaml
```

**Verbose output:**
```bash
python generate_contextual_tests_v002.py "../input/reqifz_files" --verbose
```

### Testing and Validation
```bash
# Run pytest if available
pytest

# Type checking with mypy
mypy src/

# Security audit
pip-audit
safety check
```

## Architecture

### Core Components

**Main Script:** `generate_contextual_tests_v002.py`
- Entry point for the application
- Handles REQIFZ file processing and test case generation
- Integrates Ollama API client with YAML prompt management
- Uses type aliases for better code clarity (`JSONObj`, `Table`, `Artifact`, etc.)

**Configuration Management:** `config.py`
- Centralized configuration using dataclasses
- Four main config sections: `OllamaConfig`, `StaticTestConfig`, `FileProcessingConfig`, `LoggingConfig`
- Environment variable support with defaults
- Configuration presets for development/production/testing environments
- YAML-based configuration loading via `ConfigManager`

**YAML Prompt Manager:** `yaml_prompt_manager.py`
- External template management system
- Automatic template selection and variable substitution
- Template validation and testing capabilities
- Integrates with `prompts/` directory structure

### Directory Structure

**Source Code:** `src/`
- Main Python modules
- Configuration files
- Primary execution scripts

**Prompts System:** `prompts/`
- `config/` - YAML configuration for prompt templates  
- `templates/` - Template definitions for different test case types
- `examples/` - Example prompts and usage patterns
- `tools/` - Validation utilities and helper tools

**Dependencies:** `utilities/`
- `requirements.txt` - Production dependencies with version constraints
- Helper utilities and mock data generators

### Key Features

**REQIF Processing:**
- Supports REQIFZ (compressed REQIF) file format
- XML parsing with namespace handling
- Table extraction and validation
- Artifact type classification: Heading, Information, System Interface, System Requirement

**AI Integration:**
- Ollama API client with configurable models
- Default models: `llama3.1:8b` (synthesizer), `deepseek-coder-v2:16b` (decomposer)
- Temperature control (default: 0.0 for consistent output)
- Retry logic and timeout handling

**Test Case Generation:**
- Context-aware test case synthesis
- JIRA-compatible output format (CSV)
- Static test parameters (voltage preconditions, project keys, etc.)
- Multiple output formats and encoding options

**Configuration System:**
- Environment variable integration
- YAML configuration files
- Runtime configuration validation
- Preset configurations for different environments

## Development Notes

### Python Version Requirements
- Minimum: Python 3.13.5+
- Uses modern Python features (PEP 695 type aliases, enhanced error handling)
- Type hints throughout codebase

### External Dependencies
- **pandas** - DataFrame operations and CSV export
- **requests** - Ollama API communication
- **PyYAML** - Configuration and template management
- **click** - CLI framework (if using command line interface)
- **rich** - Terminal formatting and progress bars

### Code Patterns
- Enum classes for type safety (`ArtifactType`)
- Dataclasses for configuration management
- Type aliases for complex nested structures
- Property methods for computed values
- Context managers for resource handling
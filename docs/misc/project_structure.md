# AI Test Case Generator - File & Folder Structure Documentation

## 📋 **Project Overview**
This is an AI-powered automotive test case generator that processes REQIFZ files and generates test cases using local AI models (Ollama) with YAML-based prompt management.

---

## 📁 **COMPLETE DIRECTORY TREE**

```
AI_TC_Generator_v01/
├── .github/
│   └── workflows/
│       ├── release.yml
│       ├── update-docs.yml
│       ├── validate-and-test.yml
│       └── version-checker.yaml
├── docs/
│   └── misc/
│       ├── Commands.txt
│       ├── Folder_Structure.txt
│       ├── JIRA_Requirement_Artifact_Types_v1.txt
│       ├── JIRA_Requirement_Artifact_Types_v2.txt
│       ├── Laptop_Hardware_Spec.txt
│       ├── PROMPT_Bank.md
│       ├── Readme.txt
│       └── Ubuntu_Installation_Setup.txt
├── input/
│   └── Reqifz_Files/
│       └── sampe_requiremenr.reqif
├── output/
│   └── TCD/
│       └── README.md
├── prompts/
│   ├── config/
│   │   ├── .gitkeep
│   │   ├── README.md
│   │   └── prompt_config.yaml
│   ├── examples/
│   │   ├── .gitkeep
│   │   └── README.md
│   ├── templates/
│   │   ├── .gitkeep
│   │   ├── README.md
│   │   ├── error_handling.yaml
│   │   ├── test_generation_v1_default.yaml
│   │   └── test_generation_v2_structured.yaml
│   ├── tools/
│   │   ├── .gitkeep
│   │   ├── README.md
│   │   └── validation_and_tools.py
│   └── prompt_documentation.md
├── samples/
│   └── TCD/
│       └── README.md
├── src/
│   ├── config.py
│   ├── example_config.yaml
│   ├── generate_contextual_tests_v001.py
│   ├── generate_contextual_tests_v002.py
│   └── yaml_prompt_manager.py
├── utilities/
│   ├── create_mock_reqifz.py
│   ├── requirements.txt
│   └── version_check.py
├── .gitignore
├── installation.md
├── JIRA_Requirement_Artifact_Types.txt
└── README.md
```

---

## 🏗️ **MAIN DIRECTORIES**

### **`.github/workflows/`** - CI/CD Automation
**Purpose**: GitHub Actions workflows for automated testing, validation, and releases

| File | Purpose |
|------|---------|
| `validate-and-test.yml` | Main CI pipeline with Python 3.13.5+ validation |
| `version-checker.yaml` | Multi-platform Python version enforcement |
| `release.yml` | Automated release packaging and GitHub releases |
| `update-docs.yml` | Auto-generates documentation from templates |

### **`docs/misc/`** - Project Documentation
**Purpose**: Legacy documentation, setup guides, and reference materials

| File | Purpose |
|------|---------|
| `JIRA_Requirement_Artifact_Types_v2.txt` | Automotive requirement artifact definitions |
| `Ubuntu_Installation_Setup.txt` | Linux installation and setup guide |
| `Commands.txt` | Command reference and usage examples |
| `Folder_Structure.txt` | Original project structure notes |
| `PROMPT_Bank.md` | Prompt development reference |

### **`input/Reqifz_Files/`** ⭐ **INPUT DIRECTORY**
**Purpose**: Folder where all the REQIFZ files are stored. New REQIFZ files will be added here.
- **Usage**: Place your automotive requirements files (.reqifz format) in this directory for processing
- **Format**: REQIFZ (zipped REQIF) files containing automotive system requirements
- **Example**: Door control systems, window control, rental car mode requirements

### **`output/TCD/`** ⭐ **OUTPUT DIRECTORY**
**Purpose**: Folder where the generated TCD (Test Case Design) files are stored
- **Format**: CSV files with comprehensive test cases
- **Naming**: `{filename}_TCD_{model}_YAML.csv`
- **Contents**: Issue ID, Summary, Test Steps, Expected Results, etc.

### **`prompts/`** - AI Prompt Management System
**Purpose**: YAML-based prompt template system for customizing AI behavior

#### **`prompts/config/`**
| File | Purpose |
|------|---------|
| `prompt_config.yaml` | Central configuration for prompt system |

#### **`prompts/templates/`**
| File | Purpose |
|------|---------|
| `test_generation_v2_structured.yaml` | Active prompt templates (current) |
| `test_generation_v1_default.yaml` | Legacy v001 prompts in YAML format |
| `error_handling.yaml` | Error message templates and guidance |

#### **`prompts/tools/`**
| File | Purpose |
|------|---------|
| `validation_and_tools.py` | Template validation and testing utilities |

### **`samples/TCD/`** ⭐ **SAMPLE DIRECTORY**
**Purpose**: Sample TCD files are stored here for reference and testing
- **Usage**: Example outputs to understand expected format and structure
- **Contents**: Reference test case files showing proper formatting

### **`src/`** ⭐ **SOURCE CODE DIRECTORY**
**Purpose**: Main Python scripts and application logic are stored here

| File | Purpose | Status |
|------|---------|--------|
| `generate_contextual_tests_v002.py` | **Main application** (latest version) | ⭐ **CURRENT** |
| `generate_contextual_tests_v001.py` | Original version with hardcoded prompts | Legacy |
| `yaml_prompt_manager.py` | YAML prompt template management system | ⭐ **CORE** |
| `config.py` | Comprehensive configuration management | ⭐ **CORE** |
| `example_config.yaml` | Sample configuration file | Reference |

### **`utilities/`** - Helper Tools & Scripts
**Purpose**: Supporting utilities for setup, validation, and testing

| File | Purpose |
|------|---------|
| `create_mock_reqifz.py` | Creates sample automotive REQIFZ files for testing |
| `version_check.py` | Python 3.13.5+ validation and environment checking |
| `requirements.txt` | Production-grade dependency specifications |

---

## 🎯 **KEY FILES BY IMPORTANCE**

### **⭐ ESSENTIAL FILES**

| File | Directory | Purpose |
|------|-----------|---------|
| `generate_contextual_tests_v002.py` | `src/` | **Main application** - Latest version with YAML prompts |
| `yaml_prompt_manager.py` | `src/` | **Prompt system** - Template loading and management |
| `test_generation_v2_structured.yaml` | `prompts/templates/` | **Active templates** - Current AI prompts |
| `prompt_config.yaml` | `prompts/config/` | **Prompt configuration** - Template selection rules |
| `create_mock_reqifz.py` | `utilities/` | **Test data generator** - Creates sample files |

### **📋 CONFIGURATION FILES**

| File | Directory | Purpose |
|------|-----------|---------|
| `config.py` | `src/` | Python configuration classes |
| `example_config.yaml` | `src/` | Sample configuration file |
| `requirements.txt` | `utilities/` | Python dependencies |
| `prompt_config.yaml` | `prompts/config/` | Prompt system settings |

### **📚 DOCUMENTATION FILES**

| File | Directory | Purpose |
|------|-----------|---------|
| `README.md` | Root | Main project documentation |
| `installation.md` | Root | Installation instructions |
| `prompt_documentation.md` | `prompts/` | Complete YAML prompt guide |

---

## 🔄 **DATA FLOW DIAGRAM**

```
Input Files                Processing               Output Files
    ↓                          ↓                        ↓
input/Reqifz_Files/    →    src/ + prompts/    →    output/TCD/
    │                          │                        │
    │                          ↓                        │
    │                   utilities/ (support)             │
    │                          │                        │
    └────────────────→    samples/TCD/ ←─────────────────┘
                         (reference examples)
```

---

## 📝 **DIRECTORY USAGE GUIDE**

### **For Development:**
1. **`src/`** - Modify main application logic
2. **`prompts/templates/`** - Customize AI behavior via YAML
3. **`utilities/`** - Use helper scripts for setup and testing
4. **`.github/workflows/`** - CI/CD pipeline configuration

### **For Daily Use:**
1. **`input/Reqifz_Files/`** - Place your REQIFZ files here
2. **`output/TCD/`** - Check here for generated test cases
3. **`samples/TCD/`** - Reference for expected output format

### **For Setup:**
1. **`utilities/version_check.py`** - Validate Python version
2. **`utilities/requirements.txt`** - Install dependencies
3. **`utilities/create_mock_reqifz.py`** - Generate test data

---

## 🚀 **QUICK START WORKFLOW**

### **1. Environment Setup**
```bash
# Validate Python version (requires 3.13.5+)
python utilities/version_check.py --strict

# Install dependencies
pip install -r utilities/requirements.txt

# Validate installation
python src/generate_contextual_tests_v002.py --validate-prompts
```

### **2. Generate Test Data**
```bash
# Create sample REQIFZ file
python utilities/create_mock_reqifz.py

# This creates: automotive_door_window_system.reqifz
```

### **3. Process Requirements**
```bash
# Basic usage with auto-template selection
python src/generate_contextual_tests_v002.py input.reqifz

# With specific model
python src/generate_contextual_tests_v002.py input.reqifz --model deepseek-coder-v2:16b

# List available templates
python src/generate_contextual_tests_v002.py --list-templates
```

### **4. Check Output**
- Generated CSV files appear in the same directory as input files
- Also check `output/TCD/` for organized storage
- Reference `samples/TCD/` for format examples

---

## 🔧 **CUSTOMIZATION POINTS**

### **Modify AI Behavior:**
- Edit `prompts/templates/test_generation_v2_structured.yaml`
- Adjust `prompts/config/prompt_config.yaml` for selection rules

### **Change Configuration:**
- Modify `src/config.py` for application settings
- Use `src/example_config.yaml` as reference

### **Add New Features:**
- Extend `src/generate_contextual_tests_v002.py`
- Add utilities in `utilities/` directory

---

## 📊 **FILE SIZE & COMPLEXITY**

| Category | File Count | Key Components |
|----------|------------|----------------|
| **Source Code** | 5 files | Main app, config, prompt manager |
| **Templates** | 3 files | YAML prompts, error handling |
| **Utilities** | 3 files | Mock data, validation, dependencies |
| **Documentation** | 10+ files | Setup guides, references |
| **CI/CD** | 4 files | Automated testing and releases |

---

## 🎯 **MAINTENANCE NOTES**

### **Regular Updates:**
- **`prompts/templates/`** - Update AI prompts based on testing results
- **`utilities/requirements.txt`** - Keep dependencies current
- **`.github/workflows/`** - Maintain CI/CD pipelines

### **Version Control:**
- All prompt changes are tracked in git
- Configuration changes require testing
- Use `--validate-prompts` before committing template changes

### **Backup Important Data:**
- **`input/Reqifz_Files/`** - Your source requirements
- **`output/TCD/`** - Generated test cases
- **Custom configurations** - Any modified settings

This structure supports a complete automotive test case generation workflow with modern Python practices, comprehensive validation, and maintainable YAML-based prompt management.

# YAML Prompt Management System

## Overview

The AI Test Case Generator now uses external YAML files for prompt management, allowing non-technical users to update prompts without modifying code.

## Directory Structure

```
prompts/
├── templates/              # YAML template files
│   ├── test_generation.yaml
│   └── error_handling.yaml
├── config/                 # Configuration files
│   └── prompt_config.yaml
├── examples/               # Documentation and examples
│   ├── README.md
│   └── sample_outputs/
└── tools/                  # Validation and testing tools
    └── validate_and_test.py
```

## Quick Start

### 1. Basic Usage (Auto-Selection)
```bash
# Use automatic template selection based on content
python src/generate_contextual_tests_v001.py input.reqifz
```

### 2. Specific Template Usage
```bash
# Use a specific prompt template
python src/generate_contextual_tests_v001.py input.reqifz --template door_control_specialized
```

### 3. List Available Templates
```bash
# See all available prompt templates
python src/generate_contextual_tests_v001.py --list-templates
```

### 4. Validate Templates
```bash
# Validate all prompt template files
python src/generate_contextual_tests_v001.py --validate-prompts
```

## Available Templates

### Test Generation Templates

1. **automotive_default**
   - General purpose automotive testing prompt
   - Used as fallback for unknown requirement types
   - Suitable for most standard automotive requirements

2. **door_control_specialized**
   - Specialized for door control and locking systems
   - Emphasizes safety-critical scenarios
   - Auto-selected for requirements containing: "door", "lock", "DCS"

3. **window_control_specialized**
   - Specialized for window control with rain detection
   - Focuses on weather response and safety features
   - Auto-selected for requirements containing: "window", "rain", "WCS"

## Editing Templates

### Template Structure
```yaml
template_name:
  name: "Human-readable name"
  description: "Description of when to use this template"
  category: "general|specialized"
  tags: ["tag1", "tag2"]
  
  variables:
    required: ["var1", "var2"]     # Must be provided
    optional: ["var3", "var4"]     # Can be omitted
    defaults:
      var3: "default value"        # Used if not provided
  
  template: |
    Your prompt text with {variable} substitution.
    Use {var1} and {var2} in your prompt.
    Optional variables: {var3}
```

### Variable Substitution
- Use `{variable_name}` format for variable placeholders
- Required variables must be provided or an error occurs
- Optional variables use defaults if not provided
- Variables are substituted as simple string replacement

### Available Variables

All test generation templates have access to these variables:

- `heading`: Current section heading from REQIF
- `requirement_id`: Requirement identifier
- `table_str`: Formatted table data with headers and rows
- `row_count`: Number of data rows in the table
- `voltage_precondition`: Standard precondition text
- `info_str`: Additional information context (optional)
- `interface_str`: System interface definitions (optional)

## Auto-Selection Rules

Templates are automatically selected based on:

1. **Heading Keywords**: Words in the feature heading
   - "door", "lock" → door_control_specialized
   - "window", "rain" → window_control_specialized

2. **Requirement ID Patterns**: Patterns in requirement IDs
   - "DCS", "DOOR" → door_control_specialized
   - "WCS", "WINDOW" → window_control_specialized

3. **Default Fallback**: automotive_default for unmatched requirements

## Creating New Templates

### Step 1: Add Template to YAML
Edit `prompts/templates/test_generation.yaml`:

```yaml
my_new_template:
  name: "My New Template"
  description: "Template for specific use case"
  category: "specialized"
  tags: ["custom", "specialized"]
  
  variables:
    required: ["heading", "requirement_id", "table_str", "row_count", "voltage_precondition"]
    optional: ["info_str", "interface_str"]
    defaults:
      info_str: "Default information"
      interface_str: "Default interfaces"
  
  template: |
    You are an expert in my specific domain...
    {heading}
    {requirement_id}
    {table_str}
    # ... your custom prompt content
```

### Step 2: Add Selection Rules (Optional)
Add auto-selection rules in the same file:

```yaml
prompt_selection:
  heading_keywords:
    my_domain:
      keywords: ["keyword1", "keyword2"]
      template: "my_new_template"
  
  requirement_id_patterns:
    my_patterns:
      patterns: ["MYID", "CUSTOM"]
      template: "my_new_template"
```

### Step 3: Test Your Template
```bash
# Validate the new template
python src/generate_contextual_tests_v001.py --validate-prompts

# Test with specific template
python src/generate_contextual_tests_v001.py input.reqifz --template my_new_template
```

## Configuration

### Main Configuration (`prompts/config/prompt_config.yaml`)

Key settings you can modify:

```yaml
# Default template when auto-selection fails
defaults:
  template_selection: "automotive_default"

# Enable/disable auto-selection
auto_selection:
  enabled: true
  fallback_to_default: true

# Model-specific preferences
model_configurations:
  "llama3.1:8b":
    recommended_templates: ["automotive_default", "door_control_specialized"]
  "deepseek-coder-v2:16b":
    recommended_templates: ["door_control_specialized", "window_control_specialized"]
```

## Troubleshooting

### Common Issues

1. **Template Not Found**
   ```
   ❌ Template 'my_template' not found
   ```
   - Check template name spelling
   - Verify template exists in `prompts/templates/test_generation.yaml`
   - Use `--list-templates` to see available templates

2. **Missing Required Variables**
   ```
   ❌ Missing required variables: ['heading', 'requirement_id']
   ```
   - Check template's `variables.required` section
   - Ensure all required variables are provided
   - This is usually an internal error, contact support

3. **YAML Syntax Errors**
   ```
   ❌ YAML syntax error: invalid indentation
   ```
   - Check YAML file formatting
   - Ensure consistent indentation (spaces, not tabs)
   - Use `--validate-prompts` to check syntax

4. **Template Rendering Errors**
   ```
   ❌ Template rendering error: variable not found
   ```
   - Check for typos in variable names
   - Ensure all `{variable_name}` placeholders are valid
   - Variables are case-sensitive

### Validation Commands

```bash
# Check all template files for errors
python src/generate_contextual_tests_v001.py --validate-prompts

# Test template rendering
python prompts/tools/validate_and_test.py

# List available templates and their info
python src/generate_contextual_tests_v001.py --list-templates
```

## Best Practices

### Template Design

1. **Be Specific**: Specialized templates should focus on domain-specific requirements
2. **Use Context**: Leverage all available variables for better AI responses
3. **Safety First**: For automotive templates, emphasize safety-critical scenarios
4. **Clear Instructions**: Provide explicit, numbered instructions to the AI
5. **Consistent Format**: Maintain consistent output format requirements

### Variable Usage

```yaml
# Good: Use all available context
template: |
  You are an expert in {heading} systems.
  
  Context Information: {info_str}
  System Interfaces: {interface_str}
  
  Requirement: {requirement_id}
  Test {row_count} scenarios from: {table_str}

# Bad: Ignore available context
template: |
  Generate test cases for {requirement_id}.
  {table_str}
```

### Template Organization

1. **Name Consistently**: Use `domain_purpose` format (e.g., `door_control_specialized`)
2. **Document Purpose**: Clear description and tags for each template
3. **Group Related**: Keep similar templates together in YAML files
4. **Version Control**: Track template changes in git with clear commit messages

## Integration with Existing Code

### Backward Compatibility

The YAML prompt system maintains full backward compatibility:

- Existing scripts work without modification
- Output format remains identical
- All command-line options preserved
- Performance impact is minimal

### Output File Changes

Files generated with YAML prompts use `_YAML` suffix:
- Old: `file_TCD_llama3_1_8b_Final.csv`
- New: `file_TCD_llama3_1_8b_YAML.csv`

This allows easy comparison between old and new prompt systems.

## Development and Testing

### Hot Reload (Development)

```bash
# Reload templates without restarting
python src/generate_contextual_tests_v001.py --reload-prompts
```

### Testing New Templates

1. **Create Template**: Add to YAML file
2. **Validate**: Run `--validate-prompts`
3. **Test Rendering**: Use validation tools
4. **Test with Real Data**: Process small REQIFZ file
5. **Compare Results**: Check output quality

### Sample Test Data

```python
# Use this data structure for testing templates
sample_data = {
    'heading': 'Door Control System - Safety Features',
    'requirement_id': 'REQ_DCS_001',
    'table_str': '''Headers: Input1, Input2, Output1
Row 1: ['0', '0', '0']
Row 2: ['1', '1', '1']''',
    'row_count': 2,
    'voltage_precondition': '1. Voltage= 12V\\n2. Bat-ON',
    'info_str': 'Focus on safety-critical scenarios',
    'interface_str': 'B_INPUT1: Description, B_INPUT2: Description'
}
```

## Migration from Hardcoded Prompts

### What Changed

1. **Prompts Externalized**: Moved from Python code to YAML files
2. **Auto-Selection Added**: Templates chosen based on content
3. **Template Validation**: Built-in validation and testing tools
4. **Hot Reload**: Templates can be updated without code changes

### Migration Benefits

- ✅ Non-technical users can edit prompts
- ✅ No code deployments needed for prompt updates
- ✅ A/B testing different prompt variations
- ✅ Version control for prompt changes
- ✅ Template validation and testing tools
- ✅ Specialized prompts for different domains

### Rollback Plan

If needed, you can temporarily revert to hardcoded prompts by:

1. Keep backup of original files
2. Use git to revert changes
3. Or modify code to skip YAML prompt manager

## Support and Maintenance

### Regular Maintenance

1. **Review Template Performance**: Monitor success rates
2. **Update Based on Feedback**: Improve prompts based on output quality
3. **Add New Templates**: Create specialized templates for new domains
4. **Validate Regularly**: Run validation tools after changes

### Getting Help

1. **Check Documentation**: Start with this README
2. **Run Validation**: Use `--validate-prompts` for errors
3. **Test Templates**: Use validation tools in `prompts/tools/`
4. **Contact Team**: Reach out to test engineering team for support

## Advanced Features

### Template Inheritance (Future)

Plan for future template inheritance system:

```yaml
# Base template
base_automotive:
  template: |
    You are an expert automotive test engineer.
    {common_sections}

# Inherit from base
door_control_specialized:
  inherits: "base_automotive"
  template: |
    {inherited_content}
    Specialized door control instructions...
```

### Performance Monitoring (Future)

Future features planned:

- Template success rate tracking
- Response quality metrics
- Auto-optimization based on results
- Template recommendation engine

---

## Quick Reference

### Commands
```bash
# Basic usage
python src/generate_contextual_tests_v001.py input.reqifz

# With specific template
python src/generate_contextual_tests_v001.py input.reqifz --template door_control_specialized

# Management commands
python src/generate_contextual_tests_v001.py --list-templates
python src/generate_contextual_tests_v001.py --validate-prompts
python src/generate_contextual_tests_v001.py --reload-prompts

# Testing and validation
python prompts/tools/validate_and_test.py
```

### File Locations
- Templates: `prompts/templates/test_generation.yaml`
- Configuration: `prompts/config/prompt_config.yaml`
- Documentation: `prompts/examples/README.md`
- Tools: `prompts/tools/validate_and_test.py`

### Template Variables
- `{heading}` - Current section heading
- `{requirement_id}` - Requirement identifier  
- `{table_str}` - Formatted table data
- `{row_count}` - Number of data rows
- `{voltage_precondition}` - Standard precondition
- `{info_str}` - Additional information (optional)
- `{interface_str}` - System interfaces (optional)
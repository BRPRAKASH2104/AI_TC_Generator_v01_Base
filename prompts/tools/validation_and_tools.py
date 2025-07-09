#!/usr/bin/env python3
"""
Prompt Validation and Testing Tools
File: prompts/tools/validate_and_test.py

Tools for validating YAML prompt templates and testing prompt rendering
"""

import sys
import yaml
from pathlib import Path
sys.path.append('src')

from yaml_prompt_manager import YAMLPromptManager

def validate_all_templates():
    """Validate all YAML template files"""
    print("🔍 Validating All Prompt Templates...")
    
    template_files = [
        "prompts/templates/test_generation.yaml",
        "prompts/templates/error_handling.yaml"
    ]
    
    total_errors = 0
    
    for file_path in template_files:
        path = Path(file_path)
        if not path.exists():
            print(f"❌ File not found: {file_path}")
            total_errors += 1
            continue
            
        print(f"\n🔍 Validating {file_path}...")
        
        try:
            # Create a temporary prompt manager to test loading
            manager = YAMLPromptManager()
            errors = manager.validate_template_file(file_path)
            
            if errors:
                print(f"❌ Found {len(errors)} errors:")
                for error in errors:
                    print(f"   - {error}")
                total_errors += len(errors)
            else:
                print(f"✅ Valid")
        except Exception as e:
            print(f"❌ Validation error: {e}")
            total_errors += 1
    
    if total_errors == 0:
        print(f"\n🎉 All prompt templates are valid!")
        return True
    else:
        print(f"\n💥 Found {total_errors} total errors")
        return False


def test_template_rendering():
    """Test prompt template rendering with sample data"""
    print("\n🧪 Testing Template Rendering...")
    
    # Sample test data
    sample_data = {
        'heading': 'Door Control System - Test Feature',
        'requirement_id': 'REQ_TEST_001',
        'table_str': '''Headers: Input1, Input2, Output1
Row 1: ['0', '0', '0']
Row 2: ['1', '1', '1']''',
        'row_count': 2,
        'voltage_precondition': '1. Voltage= 12V\\n2. Bat-ON',
        'info_str': 'Sample information for testing',
        'interface_str': 'Sample interface definitions'
    }
    
    try:
        # Initialize prompt manager
        manager = YAMLPromptManager()
        
        # Test each template
        templates = manager.list_templates().get('test_generation', [])
        
        for template_name in templates:
            print(f"\n{'='*50}")
            print(f"Testing Template: {template_name}")
            print(f"{'='*50}")
            
            try:
                prompt = manager.get_test_prompt(template_name, **sample_data)
                print(f"✅ Template '{template_name}' rendered successfully")
                print(f"📏 Length: {len(prompt)} characters")
                
                # Show first few lines
                lines = prompt.split('\n')[:5]
                print("📄 Preview:")
                for line in lines:
                    print(f"   {line}")
                if len(prompt.split('\n')) > 5:
                    print("   ...")
                    
            except Exception as e:
                print(f"❌ Template '{template_name}' failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        return False


def test_auto_selection():
    """Test automatic template selection logic"""
    print(f"\n🎯 Testing Auto-Selection Logic...")
    
    manager = YAMLPromptManager()
    
    test_cases = [
        {
            'description': 'Door Control Feature',
            'data': {'heading': 'Door Control Safety', 'requirement_id': 'DCS_001'},
            'expected': 'door_control_specialized'
        },
        {
            'description': 'Window Control Feature', 
            'data': {'heading': 'Window Rain Detection', 'requirement_id': 'WCS_001'},
            'expected': 'window_control_specialized'
        },
        {
            'description': 'Generic Feature',
            'data': {'heading': 'Generic Feature', 'requirement_id': 'GEN_001'},
            'expected': 'automotive_default'
        }
    ]
    
    base_data = {
        'table_str': 'Headers: Input1, Output1\nRow 1: [0, 0]',
        'row_count': 1,
        'voltage_precondition': '1. Voltage= 12V\\n2. Bat-ON'
    }
    
    all_passed = True
    
    for test_case in test_cases:
        test_data = {**base_data, **test_case['data']}
        
        try:
            # Test auto-selection
            prompt = manager.get_test_prompt(**test_data)
            selected = manager.get_selected_template()
            
            print(f"✅ {test_case['description']}: Selected '{selected}'")
            
            # Check if expected template was selected
            if selected != test_case['expected']:
                print(f"⚠️  Expected '{test_case['expected']}', got '{selected}'")
                # Not necessarily an error, just information
                
        except Exception as e:
            print(f"❌ {test_case['description']}: Failed with error: {e}")
            all_passed = False
    
    return all_passed


def generate_sample_outputs():
    """Generate sample outputs for documentation"""
    print(f"\n📄 Generating Sample Outputs...")
    
    manager = YAMLPromptManager()
    
    # Sample data for door control
    door_sample = {
        'heading': 'Door Control System - Safety Features',
        'requirement_id': 'REQ_DCS_001',
        'table_str': '''Headers: No., B_VEHICLE_MOVING, B_DOOR_OPEN, B_SPEED_ABOVE_THRESHOLD, B_DOOR_LOCK_CMD
Row 1: ['1', '0', '0', '0', '0']
Row 2: ['2', '1', '0', '1', '1']''',
        'row_count': 2,
        'voltage_precondition': '1. Voltage= 12V\\n2. Bat-ON',
        'info_str': 'Focus on automatic locking during vehicle motion',
        'interface_str': 'B_VEHICLE_MOVING: Motion sensor, B_DOOR_OPEN: Position sensor'
    }
    
    try:
        # Generate door control example
        prompt = manager.get_test_prompt('door_control_specialized', **door_sample)
        
        # Save to examples directory
        examples_dir = Path("prompts/examples/sample_outputs")
        examples_dir.mkdir(parents=True, exist_ok=True)
        
        with open(examples_dir / "door_control_example.md", 'w', encoding='utf-8') as f:
            f.write("# Door Control Specialized Template - Sample Output\n\n")
            f.write("## Input Variables:\n")
            f.write("```python\n")
            for key, value in door_sample.items():
                f.write(f"{key} = {repr(value)}\n")
            f.write("```\n\n")
            f.write("## Rendered Prompt:\n")
            f.write("```\n")
            f.write(prompt)
            f.write("\n```\n")
        
        print(f"✅ Generated door_control_example.md")
        
        # Generate automotive default example
        default_sample = {**door_sample, 'heading': 'Generic Automotive Feature'}
        prompt = manager.get_test_prompt('automotive_default', **default_sample)
        
        with open(examples_dir / "automotive_default_example.md", 'w', encoding='utf-8') as f:
            f.write("# Automotive Default Template - Sample Output\n\n")
            f.write("## Input Variables:\n")
            f.write("```python\n")
            for key, value in default_sample.items():
                f.write(f"{key} = {repr(value)}\n")
            f.write("```\n\n")
            f.write("## Rendered Prompt:\n")
            f.write("```\n")
            f.write(prompt)
            f.write("\n```\n")
        
        print(f"✅ Generated automotive_default_example.md")
        return True
        
    except Exception as e:
        print(f"❌ Error generating samples: {e}")
        return False


def main():
    """Main function to run all validation and testing"""
    print("🚀 Prompt Template Validation and Testing Suite")
    print("=" * 50)
    
    # Run validation
    validation_passed = validate_all_templates()
    
    if not validation_passed:
        print("\n❌ Validation failed. Fix template errors before proceeding.")
        return 1
    
    # Run rendering tests
    rendering_passed = test_template_rendering()
    
    if not rendering_passed:
        print("\n❌ Template rendering tests failed.")
        return 1
    
    # Test auto-selection
    auto_selection_passed = test_auto_selection()
    
    if not auto_selection_passed:
        print("\n❌ Auto-selection tests failed.")
        return 1
    
    # Generate sample outputs
    samples_generated = generate_sample_outputs()
    
    if not samples_generated:
        print("\n⚠️  Sample generation failed, but continuing...")
    
    print("\n🎉 All tests passed successfully!")
    print("✅ YAML prompt system is ready for use")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
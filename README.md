# AI_TC_Generator_v01
Generate TCs from REQIF Files

## Default command:
python generate_contextual_tests.py "../input/reqifz_files"

## ✅ Enhanced Command Line Interface:
### Use different models easily:
python refactored_main_with_config.py "../input/reqifz_files" --model deepseek-coder-v2:16b

Available Models:
  - llama3.1:8b (default)
  - deepseek-coder-v2:16b
  - Or any other Ollama model you have installed
  
  
### Verbose output:
python refactored_main_with_config.py "../input/reqifz_files" --verbose

### Custom configuration:
python refactored_main_with_config.py "../input/reqifz_files" --config custom_config.yaml


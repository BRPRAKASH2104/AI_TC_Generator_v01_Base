# Basic Usage

# Process all REQIFZ files in the default directory
python ai_test_case_generator.py

# Process specific directory
python ai_test_case_generator.py --input-dir "../Reqifz_Files"

# With custom configuration
python ai_test_case_generator.py --config my_config.yaml

# Debug mode with detailed logging
python ai_test_case_generator.py --log-level DEBUG

#Command Line Options
Options:
  --input-dir PATH     Input directory containing REQIFZ files
  --output-dir PATH    Output directory for generated test cases
  --config PATH        Path to configuration file (default: config.yaml)
  --log-level TEXT     Logging level [DEBUG|INFO|WARNING|ERROR]
  --dry-run            Parse files without AI processing
  --version            Show version information
  --help               Show help message
  
#Environment Variables

# Ollama configuration
export OLLAMA_HOST=192.168.1.100
export OLLAMA_PORT=11434

# Model selection
export SYNTHESIZER_MODEL=llama3.1:8b
export DECOMPOSER_MODEL=deepseek-coder-v2:16b

# Performance tuning
export MAX_RETRIES=5
export TIMEOUT=300
export CONCURRENT_REQUESTS=4

#🧪 Testing

# Run all tests
pytest

# With coverage
pytest --cov=ai_test_case_generator

# Run specific test
pytest -k "test_parser"


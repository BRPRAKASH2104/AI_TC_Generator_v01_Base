#!/usr/bin/env python3
"""
Configuration Management for AI Test Case Generator
File: config.py

This module provides configuration classes for the AI Test Case Generator,
including settings for Ollama API, static test case parameters, and file processing.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class OllamaConfig:
    """Configuration for Ollama API connection and settings"""
    
    # Connection settings
    host: str = field(default_factory=lambda: os.getenv('OLLAMA_HOST', '127.0.0.1'))
    port: int = field(default_factory=lambda: int(os.getenv('OLLAMA_PORT', '11434')))
    timeout: int = field(default_factory=lambda: int(os.getenv('TIMEOUT', '600')))
    
    # Model settings
    temperature: float = field(default_factory=lambda: float(os.getenv('TEMPERATURE', '0.0')))
    max_retries: int = field(default_factory=lambda: int(os.getenv('MAX_RETRIES', '3')))
    concurrent_requests: int = field(default_factory=lambda: int(os.getenv('CONCURRENT_REQUESTS', '4')))
    
    # Model preferences
    synthesizer_model: str = field(default_factory=lambda: os.getenv('SYNTHESIZER_MODEL', 'llama3.1:8b'))
    decomposer_model: str = field(default_factory=lambda: os.getenv('DECOMPOSER_MODEL', 'deepseek-coder-v2:16b'))
    
    @property
    def api_url(self) -> str:
        """Get the complete API URL for Ollama"""
        return f"http://{self.host}:{self.port}/api/generate"
    
    @property
    def tags_url(self) -> str:
        """Get the URL for listing available models"""
        return f"http://{self.host}:{self.port}/api/tags"
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        try:
            # Check port range
            if not (1 <= self.port <= 65535):
                raise ValueError(f"Invalid port: {self.port}")
            
            # Check timeout
            if self.timeout <= 0:
                raise ValueError(f"Invalid timeout: {self.timeout}")
            
            # Check temperature range
            if not (0.0 <= self.temperature <= 2.0):
                raise ValueError(f"Invalid temperature: {self.temperature}")
                
            return True
        except ValueError as e:
            print(f"Configuration validation error: {e}")
            return False


@dataclass
class StaticTestConfig:
    """Static configuration for test case generation and formatting"""
    
    # Test case preconditions
    VOLTAGE_PRECONDITION: str = field(default_factory=lambda: os.getenv(
        'VOLTAGE_PRECONDITION', 
        "1. Voltage= 12V\n2. Bat-ON"
    ))
    
    # JIRA/Test management fields
    TEST_TYPE: str = field(default_factory=lambda: os.getenv('TEST_TYPE', 'RoboFIT'))
    ISSUE_TYPE: str = field(default_factory=lambda: os.getenv('ISSUE_TYPE', 'Test'))
    PROJECT_KEY: str = field(default_factory=lambda: os.getenv('PROJECT_KEY', 'TCTOIC'))
    ASSIGNEE: str = field(default_factory=lambda: os.getenv('ASSIGNEE', 'ENGG'))
    PLANNED_EXECUTION: str = field(default_factory=lambda: os.getenv('PLANNED_EXECUTION', 'Manual'))
    TEST_CASE_TYPE: str = field(default_factory=lambda: os.getenv('TEST_CASE_TYPE', 'Feature Functional'))
    COMPONENTS: str = field(default_factory=lambda: os.getenv('COMPONENTS', 'FEAT'))
    LABELS: str = field(default_factory=lambda: os.getenv('LABELS', 'SYS_DI_VALIDATION_TEST'))
    
    # Test case formatting options
    USE_ISSUE_ID_PREFIX: bool = field(default_factory=lambda: os.getenv('USE_ISSUE_ID_PREFIX', 'true').lower() == 'true')
    SUMMARY_MAX_LENGTH: int = field(default_factory=lambda: int(os.getenv('SUMMARY_MAX_LENGTH', '200')))
    DESCRIPTION_TEMPLATE: str = field(default_factory=lambda: os.getenv(
        'DESCRIPTION_TEMPLATE', 
        'Generated test case for requirement {requirement_id}'
    ))


@dataclass
class FileProcessingConfig:
    """Configuration for file processing and I/O operations"""
    
    # Input/Output settings
    INPUT_ENCODING: str = field(default_factory=lambda: os.getenv('INPUT_ENCODING', 'utf-8'))
    OUTPUT_ENCODING: str = field(default_factory=lambda: os.getenv('OUTPUT_ENCODING', 'utf-8-sig'))
    
    # REQIF processing
    REQIF_NAMESPACES: Dict[str, str] = field(default_factory=lambda: {
        'reqif': 'http://www.omg.org/spec/ReqIF/20110401/reqif.xsd',
        'html': 'http://www.w3.org/1999/xhtml'
    })
    
    # File patterns and locations
    REQIFZ_PATTERN: str = field(default_factory=lambda: os.getenv('REQIFZ_PATTERN', '*.reqifz'))
    OUTPUT_SUFFIX: str = field(default_factory=lambda: os.getenv('OUTPUT_SUFFIX', '_TCD_{model}_Final.csv'))
    BACKUP_DIRECTORY: str = field(default_factory=lambda: os.getenv('BACKUP_DIRECTORY', 'backups'))
    
    # Processing options
    VALIDATE_XML: bool = field(default_factory=lambda: os.getenv('VALIDATE_XML', 'true').lower() == 'true')
    SKIP_EMPTY_TABLES: bool = field(default_factory=lambda: os.getenv('SKIP_EMPTY_TABLES', 'true').lower() == 'true')
    MAX_TABLE_ROWS: int = field(default_factory=lambda: int(os.getenv('MAX_TABLE_ROWS', '100')))


@dataclass
class LoggingConfig:
    """Configuration for logging and monitoring"""
    
    # Log levels and settings
    LOG_LEVEL: str = field(default_factory=lambda: os.getenv('LOG_LEVEL', 'INFO'))
    LOG_TO_FILE: bool = field(default_factory=lambda: os.getenv('LOG_TO_FILE', 'false').lower() == 'true')
    LOG_DIRECTORY: str = field(default_factory=lambda: os.getenv('LOG_DIRECTORY', 'logs'))
    
    # Performance monitoring
    MONITOR_PERFORMANCE: bool = field(default_factory=lambda: os.getenv('MONITOR_PERFORMANCE', 'true').lower() == 'true')
    LOG_API_CALLS: bool = field(default_factory=lambda: os.getenv('LOG_API_CALLS', 'false').lower() == 'true')
    LOG_TEMPLATE_USAGE: bool = field(default_factory=lambda: os.getenv('LOG_TEMPLATE_USAGE', 'true').lower() == 'true')


class ConfigManager:
    """Main configuration manager that combines all configuration classes"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file: Optional path to custom configuration file
        """
        # Initialize all configuration sections
        self.ollama = OllamaConfig()
        self.static_test = StaticTestConfig()
        self.file_processing = FileProcessingConfig()
        self.logging = LoggingConfig()
        
        # Load custom configuration if provided
        if config_file:
            self.load_from_file(config_file)
        
        # Validate configuration
        self.validate()
    
    def load_from_file(self, config_file: str) -> None:
        """
        Load configuration from YAML file
        
        Args:
            config_file: Path to configuration file
        """
        try:
            import yaml
            config_path = Path(config_file)
            
            if not config_path.exists():
                print(f"Warning: Config file not found: {config_file}")
                return
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            self.update_from_dict(config_data)
            print(f"✅ Loaded configuration from: {config_file}")
            
        except Exception as e:
            print(f"Warning: Failed to load config file {config_file}: {e}")
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """
        Update configuration from dictionary
        
        Args:
            config_dict: Dictionary containing configuration updates
        """
        # Update Ollama configuration
        if 'ollama' in config_dict:
            ollama_config = config_dict['ollama']
            for key, value in ollama_config.items():
                if hasattr(self.ollama, key):
                    setattr(self.ollama, key, value)
        
        # Update static test configuration
        if 'static_test' in config_dict:
            static_config = config_dict['static_test']
            for key, value in static_config.items():
                if hasattr(self.static_test, key):
                    setattr(self.static_test, key, value)
        
        # Update file processing configuration
        if 'file_processing' in config_dict:
            file_config = config_dict['file_processing']
            for key, value in file_config.items():
                if hasattr(self.file_processing, key):
                    setattr(self.file_processing, key, value)
        
        # Update logging configuration
        if 'logging' in config_dict:
            logging_config = config_dict['logging']
            for key, value in logging_config.items():
                if hasattr(self.logging, key):
                    setattr(self.logging, key, value)
    
    def validate(self) -> bool:
        """
        Validate all configuration sections
        
        Returns:
            True if all configurations are valid
        """
        validations = [
            self.ollama.validate(),
            # Add other validation methods as needed
        ]
        
        return all(validations)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary
        
        Returns:
            Dictionary representation of all configuration
        """
        return {
            'ollama': {
                'host': self.ollama.host,
                'port': self.ollama.port,
                'timeout': self.ollama.timeout,
                'temperature': self.ollama.temperature,
                'max_retries': self.ollama.max_retries,
                'concurrent_requests': self.ollama.concurrent_requests,
                'synthesizer_model': self.ollama.synthesizer_model,
                'decomposer_model': self.ollama.decomposer_model
            },
            'static_test': {
                'VOLTAGE_PRECONDITION': self.static_test.VOLTAGE_PRECONDITION,
                'TEST_TYPE': self.static_test.TEST_TYPE,
                'ISSUE_TYPE': self.static_test.ISSUE_TYPE,
                'PROJECT_KEY': self.static_test.PROJECT_KEY,
                'ASSIGNEE': self.static_test.ASSIGNEE,
                'PLANNED_EXECUTION': self.static_test.PLANNED_EXECUTION,
                'TEST_CASE_TYPE': self.static_test.TEST_CASE_TYPE,
                'COMPONENTS': self.static_test.COMPONENTS,
                'LABELS': self.static_test.LABELS
            },
            'file_processing': {
                'INPUT_ENCODING': self.file_processing.INPUT_ENCODING,
                'OUTPUT_ENCODING': self.file_processing.OUTPUT_ENCODING,
                'REQIFZ_PATTERN': self.file_processing.REQIFZ_PATTERN,
                'OUTPUT_SUFFIX': self.file_processing.OUTPUT_SUFFIX,
                'VALIDATE_XML': self.file_processing.VALIDATE_XML,
                'SKIP_EMPTY_TABLES': self.file_processing.SKIP_EMPTY_TABLES,
                'MAX_TABLE_ROWS': self.file_processing.MAX_TABLE_ROWS
            },
            'logging': {
                'LOG_LEVEL': self.logging.LOG_LEVEL,
                'LOG_TO_FILE': self.logging.LOG_TO_FILE,
                'LOG_DIRECTORY': self.logging.LOG_DIRECTORY,
                'MONITOR_PERFORMANCE': self.logging.MONITOR_PERFORMANCE,
                'LOG_API_CALLS': self.logging.LOG_API_CALLS,
                'LOG_TEMPLATE_USAGE': self.logging.LOG_TEMPLATE_USAGE
            }
        }
    
    def save_to_file(self, config_file: str) -> None:
        """
        Save current configuration to YAML file
        
        Args:
            config_file: Path where to save configuration
        """
        try:
            import yaml
            config_path = Path(config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)
            
            print(f"✅ Configuration saved to: {config_file}")
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def print_summary(self) -> None:
        """Print a summary of current configuration"""
        print("\n" + "=" * 50)
        print("CONFIGURATION SUMMARY")
        print("=" * 50)
        
        print(f"\n🔗 OLLAMA CONNECTION:")
        print(f"  • Host: {self.ollama.host}:{self.ollama.port}")
        print(f"  • API URL: {self.ollama.api_url}")
        print(f"  • Timeout: {self.ollama.timeout}s")
        print(f"  • Temperature: {self.ollama.temperature}")
        print(f"  • Default Models: {self.ollama.synthesizer_model}, {self.ollama.decomposer_model}")
        
        print(f"\n📋 TEST CASE SETTINGS:")
        print(f"  • Test Type: {self.static_test.TEST_TYPE}")
        print(f"  • Project Key: {self.static_test.PROJECT_KEY}")
        print(f"  • Assignee: {self.static_test.ASSIGNEE}")
        print(f"  • Execution: {self.static_test.PLANNED_EXECUTION}")
        
        print(f"\n📁 FILE PROCESSING:")
        print(f"  • Input Encoding: {self.file_processing.INPUT_ENCODING}")
        print(f"  • Output Encoding: {self.file_processing.OUTPUT_ENCODING}")
        print(f"  • Validate XML: {self.file_processing.VALIDATE_XML}")
        print(f"  • Max Table Rows: {self.file_processing.MAX_TABLE_ROWS}")
        
        print(f"\n📊 LOGGING:")
        print(f"  • Log Level: {self.logging.LOG_LEVEL}")
        print(f"  • Log to File: {self.logging.LOG_TO_FILE}")
        print(f"  • Monitor Performance: {self.logging.MONITOR_PERFORMANCE}")
        
        print("=" * 50)


# Global configuration instance (optional convenience)
default_config = ConfigManager()


# Configuration presets for different environments
class ConfigPresets:
    """Predefined configuration presets for different environments"""
    
    @staticmethod
    def development() -> ConfigManager:
        """Configuration preset for development environment"""
        config = ConfigManager()
        config.logging.LOG_LEVEL = "DEBUG"
        config.logging.LOG_TO_FILE = True
        config.logging.MONITOR_PERFORMANCE = True
        config.ollama.timeout = 300  # Shorter timeout for dev
        return config
    
    @staticmethod
    def production() -> ConfigManager:
        """Configuration preset for production environment"""
        config = ConfigManager()
        config.logging.LOG_LEVEL = "INFO"
        config.logging.LOG_TO_FILE = True
        config.logging.MONITOR_PERFORMANCE = False
        config.ollama.timeout = 600  # Longer timeout for production
        config.ollama.max_retries = 5
        return config
    
    @staticmethod
    def testing() -> ConfigManager:
        """Configuration preset for testing environment"""
        config = ConfigManager()
        config.logging.LOG_LEVEL = "DEBUG"
        config.logging.LOG_TO_FILE = False
        config.ollama.timeout = 120  # Very short timeout for tests
        config.file_processing.MAX_TABLE_ROWS = 10  # Limit for test data
        return config


if __name__ == "__main__":
    # Demo configuration usage
    print("🔧 AI Test Case Generator - Configuration Demo")
    
    # Create default configuration
    config = ConfigManager()
    
    # Print summary
    config.print_summary()
    
    # Save example configuration
    config.save_to_file("example_config.yaml")
    
    # Test different presets
    print("\n🧪 TESTING PRESETS:")
    dev_config = ConfigPresets.development()
    print(f"Development timeout: {dev_config.ollama.timeout}s")
    
    prod_config = ConfigPresets.production()
    print(f"Production timeout: {prod_config.ollama.timeout}s")
    
    test_config = ConfigPresets.testing()
    print(f"Testing timeout: {test_config.ollama.timeout}s")

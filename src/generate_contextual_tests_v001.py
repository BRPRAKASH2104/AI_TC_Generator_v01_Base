# =================================================================
#  Context-Rich, High-Performance Test Case Generator
#  Version: Refactored v1.1 - With External Configuration
#
#  IMPROVEMENTS:
#  - Separated concerns into dedicated classes
#  - External configuration management
#  - Created modular, reusable components
#  - Maintained 100% backward compatibility
#  - Added command line model selection
# =================================================================

import zipfile
import xml.etree.ElementTree as ET
import requests
import json
import pandas as pd
from pathlib import Path
import argparse
import re
from typing import List, Dict, Optional, Any

# Import configuration (assumes config.py is in the same directory)
try:
    from config import ConfigManager, StaticTestConfig, OllamaConfig
except ImportError:
    # Fallback to inline configuration if config.py is not available
    from dataclasses import dataclass
    import os
    
    @dataclass
    class StaticTestConfig:
        VOLTAGE_PRECONDITION: str = "1. Voltage= 12V\n2. Bat-ON"
        TEST_TYPE: str = "RoboFIT"
        ISSUE_TYPE: str = "Test"
        PROJECT_KEY: str = "TCTOIC"
        ASSIGNEE: str = "ENGG"
        PLANNED_EXECUTION: str = "Manual"
        TEST_CASE_TYPE: str = "Feature Functional"
        COMPONENTS: str = "FEAT"
        LABELS: str = "SYS_DI_VALIDATION_TEST"
    
    @dataclass
    class OllamaConfig:
        host: str = "127.0.0.1"
        port: int = 11434
        timeout: int = 600
        temperature: float = 0.0
        
        @property
        def api_url(self) -> str:
            return f"http://{self.host}:{self.port}/api/generate"
    
    class ConfigManager:
        def __init__(self):
            self.static_test = StaticTestConfig()
            self.ollama = OllamaConfig()


# =================================================================
# OLLAMA API CLIENT
# =================================================================

class OllamaClient:
    """Handles all interactions with Ollama API"""
    
    def __init__(self, config: OllamaConfig = None):
        self.config = config or OllamaConfig()
        self.proxies = {"http": None, "https": None}
    
    def generate_response(self, model_name: str, prompt: str, is_json: bool = False) -> str:
        """
        Generate response from Ollama model
        
        Args:
            model_name: Name of the model to use
            prompt: Input prompt for the model
            is_json: Whether to request JSON format response
            
        Returns:
            Generated response as string
        """
        print(f"      - Calling model '{model_name}' (deterministic mode)...")
        
        payload = {
            "model": model_name, 
            "prompt": prompt, 
            "stream": False, 
            "options": {"temperature": self.config.temperature}
        }
        
        if is_json:
            payload["format"] = "json"
        
        try:
            response = requests.post(
                self.config.api_url, 
                json=payload, 
                proxies=self.proxies, 
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return json.loads(response.text).get("response", "")
        except Exception as e:
            print(f"  -> OLLAMA API ERROR with model {model_name}: {e}")
            return ""


# =================================================================
# JSON RESPONSE PARSER
# =================================================================

class JSONResponseParser:
    """Handles parsing JSON responses from AI models"""
    
    @staticmethod
    def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
        """
        Extract and parse JSON from AI model response
        
        Args:
            response_text: Raw response text from model
            
        Returns:
            Parsed JSON dictionary or None if parsing fails
        """
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            return None
        except (json.JSONDecodeError, IndexError):
            return None


# =================================================================
# HTML TABLE PARSER
# =================================================================

class HTMLTableParser:
    """Handles parsing of HTML tables from REQIF XML content"""
    
    def __init__(self, namespaces: Dict[str, str]):
        self.namespaces = namespaces
    
    def parse_html_table(self, table_element) -> Optional[Dict[str, Any]]:
        """
        Parse HTML table element into structured data
        
        Args:
            table_element: XML table element
            
        Returns:
            Dictionary with 'headers' and 'rows' keys, or None if parsing fails
        """
        headers, data_rows = [], []
        raw_rows = table_element.findall('.//html:tr', self.namespaces)
        
        if not raw_rows:
            return None
        
        # Create grid to handle colspan/rowspan
        grid = [[] for _ in range(len(raw_rows))]
        
        # Process each row and cell
        for r, tr in enumerate(raw_rows):
            for td in tr.findall('.//html:td', self.namespaces) + tr.findall('.//html:th', self.namespaces):
                c = 0
                while c < len(grid[r]):
                    c += 1
                
                text = ''.join(td.itertext()).strip()
                colspan = int(td.get('colspan', 1))
                rowspan = int(td.get('rowspan', 1))
                
                # Fill grid cells for colspan/rowspan
                for i in range(r, r + rowspan):
                    j_start = c 
                    while len(grid[i]) < j_start + colspan:
                        grid[i].append('')
                    for j in range(j_start, j_start + colspan):
                        grid[i][j] = text
        
        # Fill empty cells with previous row values
        for r_idx, row in enumerate(grid):
            for c_idx, cell in enumerate(row):
                if cell == '' and r_idx > 0 and c_idx < len(grid[r_idx-1]):
                    grid[r_idx][c_idx] = grid[r_idx-1][c_idx]
        
        # Process headers and data rows
        if len(grid) >= 2:
            header_row1, header_row2 = grid[0], grid[1]
            data_rows = grid[2:]
            merged_headers = []
            
            c = 0
            while c < len(header_row1):
                span_text = header_row1[c]
                span_count = 1
                
                while (c + span_count < len(header_row1) and 
                       header_row1[c + span_count] == span_text):
                    span_count += 1
                
                if span_text and span_text not in ["Input", "Output", "No."]:
                    for i in range(span_count):
                        merged_headers.append(header_row2[c+i])
                else:
                    for i in range(span_count):
                        merged_headers.append(f"{span_text} - {header_row2[c+i]}")
                
                c += span_count
            
            headers = merged_headers
        
        return {'headers': headers, 'rows': data_rows}


# =================================================================
# REQIF ARTIFACT EXTRACTOR
# =================================================================

class REQIFArtifactExtractor:
    """Handles extraction of artifacts from REQIFZ files"""
    
    def __init__(self, namespaces: Dict[str, str] = None):
        self.namespaces = namespaces or {
            'reqif': 'http://www.omg.org/spec/ReqIF/20110401/reqif.xsd', 
            'html': 'http://www.w3.org/1999/xhtml'
        }
        self.table_parser = HTMLTableParser(self.namespaces)
    
    def extract_all_artifacts(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Extract all artifacts from a REQIFZ file
        
        Args:
            file_path: Path to the REQIFZ file
            
        Returns:
            List of artifact dictionaries
        """
        all_objects = []
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                reqif_filename = self._find_reqif_file(zf)
                
                with zf.open(reqif_filename) as reqif_file:
                    tree = ET.parse(reqif_file)
                    root = tree.getroot()
                    
                    # Build type mappings
                    type_map = self._build_type_map(root)
                    type_to_foreign_id_map, type_to_text_def_map = self._build_attribute_maps(root)
                    
                    # Extract all spec objects
                    for spec_object in root.findall('.//reqif:SPEC-OBJECTS//reqif:SPEC-OBJECT', self.namespaces):
                        artifact = self._process_spec_object(
                            spec_object, type_map, type_to_foreign_id_map, type_to_text_def_map
                        )
                        all_objects.append(artifact)
                        
        except Exception as e:
            print(f"  -> ERROR processing XML in '{file_path.name}': {e}")
        
        return all_objects
    
    def _find_reqif_file(self, zip_file) -> str:
        """Find the .reqif file within the ZIP archive"""
        reqif_filename = next((name for name in zip_file.namelist() if name.endswith('.reqif')), None)
        if not reqif_filename:
            raise FileNotFoundError("No .reqif file found in the archive.")
        return reqif_filename
    
    def _build_type_map(self, root) -> Dict[str, str]:
        """Build mapping from type IDs to type names"""
        return {
            t.get('IDENTIFIER'): t.get('LONG-NAME') 
            for t in root.findall('.//reqif:SPEC-OBJECT-TYPE', self.namespaces)
        }
    
    def _build_attribute_maps(self, root) -> tuple:
        """Build mappings for foreign ID and text definition attributes"""
        type_to_foreign_id_map, type_to_text_def_map = {}, {}
        
        for spec_type in root.findall('.//reqif:SPEC-OBJECT-TYPE', self.namespaces):
            type_id = spec_type.get('IDENTIFIER')
            
            foreign_id_def = spec_type.find(
                ".//reqif:ATTRIBUTE-DEFINITION-STRING[@LONG-NAME='ReqIF.ForeignID']", 
                self.namespaces
            )
            if foreign_id_def is not None:
                type_to_foreign_id_map[type_id] = foreign_id_def.get('IDENTIFIER')
            
            text_def = spec_type.find(
                ".//reqif:ATTRIBUTE-DEFINITION-XHTML[@LONG-NAME='ReqIF.Text']", 
                self.namespaces
            )
            if text_def is not None:
                type_to_text_def_map[type_id] = text_def.get('IDENTIFIER')
        
        return type_to_foreign_id_map, type_to_text_def_map
    
    def _process_spec_object(self, spec_object, type_map: Dict[str, str], 
                           foreign_id_map: Dict[str, str], text_def_map: Dict[str, str]) -> Dict[str, Any]:
        """Process a single spec object and extract its data"""
        internal_id = spec_object.get('IDENTIFIER')
        req_id, req_text, req_type, table_data = internal_id, "", "Unknown", None
        
        # Get object type
        type_ref_node = spec_object.find('reqif:TYPE/reqif:SPEC-OBJECT-TYPE-REF', self.namespaces)
        if type_ref_node is not None:
            spec_object_type_ref = type_ref_node.text
            req_type = type_map.get(spec_object_type_ref, "Unknown")
            
            # Extract attributes
            values_container = spec_object.find('reqif:VALUES', self.namespaces)
            if values_container is not None:
                req_id = self._extract_foreign_id(
                    values_container, foreign_id_map.get(spec_object_type_ref), req_id
                )
                req_text, table_data = self._extract_text_and_table(
                    values_container, text_def_map.get(spec_object_type_ref)
                )
        
        return {
            'id': req_id, 
            'text': req_text.strip(), 
            'type': req_type, 
            'table': table_data
        }
    
    def _extract_foreign_id(self, values_container, target_foreign_id_ref: str, default_id: str) -> str:
        """Extract foreign ID from values container"""
        if not target_foreign_id_ref:
            return default_id
        
        for attr_value in values_container.findall('reqif:ATTRIBUTE-VALUE-STRING', self.namespaces):
            definition_ref_node = attr_value.find(
                'reqif:DEFINITION/reqif:ATTRIBUTE-DEFINITION-STRING-REF', 
                self.namespaces
            )
            if (definition_ref_node is not None and 
                definition_ref_node.text == target_foreign_id_ref):
                return attr_value.get('THE-VALUE', default_id)
        
        return default_id
    
    def _extract_text_and_table(self, values_container, target_text_def_ref: str) -> tuple:
        """Extract text content and table data from values container"""
        if not target_text_def_ref:
            return "", None
        
        for attr_value in values_container.findall('.//reqif:ATTRIBUTE-VALUE-XHTML', self.namespaces):
            definition_ref_node = attr_value.find(
                'reqif:DEFINITION/reqif:ATTRIBUTE-DEFINITION-XHTML-REF', 
                self.namespaces
            )
            if (definition_ref_node is not None and 
                definition_ref_node.text == target_text_def_ref):
                
                the_value = attr_value.find('reqif:THE-VALUE', self.namespaces)
                if the_value is not None:
                    full_text = ''.join(the_value.itertext()).strip()
                    
                    # Check for table
                    table_element = the_value.find('.//html:table', self.namespaces)
                    table_data = None
                    if table_element is not None:
                        table_data = self.table_parser.parse_html_table(table_element)
                    
                    return full_text, table_data
        
        return "", None


# =================================================================
# TEST CASE GENERATOR
# =================================================================

class TestCaseGenerator:
    """Handles generation of test cases using AI models"""
    
    def __init__(self, model_name: str, ollama_client: OllamaClient = None, 
                 config: StaticTestConfig = None):
        self.model_name = model_name
        self.ollama_client = ollama_client or OllamaClient()
        self.config = config or StaticTestConfig()
        self.json_parser = JSONResponseParser()
    
    def generate_tests_with_context(self, requirement: Dict[str, Any], heading: str, 
                                   info_list: List[Dict[str, Any]], 
                                   interface_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate test cases for a requirement using contextual information
        
        Args:
            requirement: Requirement object with table data
            heading: Current section heading
            info_list: List of information objects for context
            interface_list: List of system interface definitions
            
        Returns:
            List of generated test case dictionaries
        """
        print(f"      - Writing test cases for '{requirement['id']}' with {self.model_name}...")
        
        table = requirement.get('table')
        if not table:
            return []
        
        # Build prompt components
        table_str = self._format_table_for_prompt(table)
        interface_str = self._format_interfaces_for_prompt(interface_list)
        info_str = self._format_info_for_prompt(info_list)
        
        # Generate prompt
        prompt = self._build_test_generation_prompt(
            requirement, heading, table_str, interface_str, info_str, len(table['rows'])
        )
        
        # Call AI model
        response_str = self.ollama_client.generate_response(self.model_name, prompt, is_json=True)
        
        # Parse response
        parsed_json = self.json_parser.extract_json_from_response(response_str)
        return parsed_json.get("test_cases", []) if parsed_json else []
    
    def _format_table_for_prompt(self, table: Dict[str, Any]) -> str:
        """Format table data for inclusion in prompt"""
        table_str = "Headers: " + ", ".join(table['headers']) + "\n"
        for i, row in enumerate(table['rows']):
            table_str += f"Row {i+1}: {row}\n"
        return table_str
    
    def _format_interfaces_for_prompt(self, interface_list: List[Dict[str, Any]]) -> str:
        """Format interface list for inclusion in prompt"""
        return "\n".join([f"- {i['id']}: {i['text']}" for i in interface_list])
    
    def _format_info_for_prompt(self, info_list: List[Dict[str, Any]]) -> str:
        """Format information list for inclusion in prompt"""
        return "\n".join([f"- {i['text']}" for i in info_list])
    
    def _build_test_generation_prompt(self, requirement: Dict[str, Any], heading: str, 
                                    table_str: str, interface_str: str, info_str: str, 
                                    row_count: int) -> str:
        """Build the complete prompt for test case generation"""
        return f"""
    You are an expert automotive test engineer. Your task is to write granular test cases by decomposing the logic table within the PRIMARY REQUIREMENT, using all the provided context.
    --- CONTEXTUAL INFORMATION ---
    ## FEATURE HEADING:
    {heading}
    ## ADDITIONAL INFORMATION NOTES:
    {info_str if info_str else "None"}
    ## SYSTEM INTERFACE DICTIONARY (Inputs/Outputs/Variables):
    {interface_str if interface_str else "None"}
    --- PRIMARY REQUIREMENT TO TEST ---
    **ID:** {requirement['id']}
    **Logic Table Data:**
    {table_str}
    --- YOUR TASK ---
    1.  Create one test case for EACH data row in the table. Ensure all {row_count} rows are covered.
    2.  Use the context to understand terms. For example, use the System Interface Dictionary to understand what a signal like 'B_FWMSIG' means.
    3.  The `"summary_suffix"` for each test case must be a short, descriptive title for that specific test row.
    4.  The `"action"` must always be "{self.config.VOLTAGE_PRECONDITION.replace("\n", "\\n")}".
    5.  The `"data"` must be a numbered list of all the "Input" column values for that row, formatted like "1) Set [Header Name] = [Value]".
    6.  The `"expected_result"` must be a concise statement combining all "Output" column values for that row, formatted as "Verify [Header Name] = [Value]".
    7.  Your entire response MUST be a single, valid JSON object with a single key: `"test_cases"`.
    """


# =================================================================
# TEST CASE FORMATTER
# =================================================================

class TestCaseFormatter:
    """Handles formatting of test cases for output"""
    
    def __init__(self, config: StaticTestConfig = None):
        self.config = config or StaticTestConfig()
    
    def format_test_case(self, test: Dict[str, Any], requirement_id: str, issue_id: int) -> Dict[str, Any]:
        """
        Format a single test case for CSV output
        
        Args:
            test: Raw test case from AI model
            requirement_id: ID of the source requirement
            issue_id: Sequential issue ID number
            
        Returns:
            Formatted test case dictionary
        """
        return {
            'Issue ID': issue_id,
            'Summary': f"[{requirement_id}] {test.get('summary_suffix', 'Generated Test')}",
            'Test Type': self.config.TEST_TYPE,
            'Issue Type': self.config.ISSUE_TYPE,
            'Project Key': self.config.PROJECT_KEY,
            'Assignee': self.config.ASSIGNEE,
            'Description': '',
            'Action': test.get('action', self.config.VOLTAGE_PRECONDITION),
            'Data': test.get('data', 'N/A'),
            'Expected Result': test.get('expected_result', 'N/A'),
            'Planned Execution': self.config.PLANNED_EXECUTION,
            'Test Case Type': self.config.TEST_CASE_TYPE,
            'Components': self.config.COMPONENTS,
            'Labels': self.config.LABELS,
            'LinkTest': requirement_id
        }


# =================================================================
# FILE PROCESSOR ORCHESTRATOR
# =================================================================

class REQIFZFileProcessor:
    """Main orchestrator for processing REQIFZ files"""
    
    def __init__(self, model_name: str, config_manager: ConfigManager = None):
        self.model_name = model_name
        self.config_manager = config_manager or ConfigManager()
        
        # Initialize components with configuration
        self.extractor = REQIFArtifactExtractor(
            getattr(self.config_manager, 'file_processing', {}).get('REQIF_NAMESPACES')
        )
        self.test_generator = TestCaseGenerator(
            model_name, 
            OllamaClient(self.config_manager.ollama),
            self.config_manager.static_test
        )
        self.formatter = TestCaseFormatter(self.config_manager.static_test)
    
    def process_file(self, reqifz_file: Path) -> None:
        """
        Process a single REQIFZ file and generate test cases
        
        Args:
            reqifz_file: Path to the REQIFZ file to process
        """
        print(f"\n===== Processing File: {reqifz_file.name} =====")
        
        # Generate output file path
        output_csv_path = self._generate_output_path(reqifz_file)
        
        # Extract artifacts
        all_objects = self.extractor.extract_all_artifacts(reqifz_file)
        if not all_objects:
            print("  -> No objects found in the file. Skipping.")
            return
        
        # Separate artifacts by type
        system_interfaces, processing_list = self._separate_artifacts(all_objects)
        print(f"  -> Found {len(system_interfaces)} 'System Interface' definitions to use as a global dictionary.")
        
        # Process artifacts and generate test cases
        master_test_list = self._process_artifacts(processing_list, system_interfaces)
        
        # Save results
        self._save_test_cases(master_test_list, output_csv_path, reqifz_file.name)
    
    def _generate_output_path(self, reqifz_file: Path) -> Path:
        """Generate output CSV file path"""
        safe_model_name = self.model_name.replace(':', '_').replace('.', '_')
        return reqifz_file.with_name(f"{reqifz_file.stem}_TCD_{safe_model_name}_Final.csv")
    
    def _separate_artifacts(self, all_objects: List[Dict[str, Any]]) -> tuple:
        """Separate artifacts into system interfaces and processing list"""
        system_interfaces = [obj for obj in all_objects if obj['type'] == 'System Interface']
        processing_list = [obj for obj in all_objects if obj['type'] != 'System Interface']
        return system_interfaces, processing_list
    
    def _process_artifacts(self, processing_list: List[Dict[str, Any]], 
                          system_interfaces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process artifacts and generate test cases"""
        master_test_list = []
        issue_id_counter = 1
        current_heading = "No Heading"
        info_since_heading = []
        
        for i, obj in enumerate(processing_list):
            if obj['type'] == 'Heading':
                current_heading = obj['text']
                info_since_heading = []
                print(f"\n  -> Context set to HEADING: '{obj['id']}'")
                continue
            
            if obj['type'] == 'Information':
                info_since_heading.append(obj)
                print(f"  -> Storing INFO: '{obj['id']}'")
                continue
            
            if obj['type'] == 'System Requirement' and obj.get('table'):
                test_cases, issue_id_counter = self._process_requirement(
                    obj, current_heading, info_since_heading, system_interfaces, 
                    i, len(processing_list), issue_id_counter
                )
                master_test_list.extend(test_cases)
                info_since_heading = []
        
        return master_test_list
    
    def _process_requirement(self, requirement: Dict[str, Any], heading: str, 
                           info_list: List[Dict[str, Any]], interface_list: List[Dict[str, Any]], 
                           index: int, total: int, issue_id_counter: int) -> tuple:
        """Process a single requirement and generate test cases"""
        print(f"  --- Analyzing Requirement {index+1}/{total} (ID: {requirement['id']}) ---")
        
        generated_tests = self.test_generator.generate_tests_with_context(
            requirement, heading, info_list, interface_list
        )
        
        if not generated_tests:
            print(f"      - AI failed to generate test cases for this table.")
            return [], issue_id_counter
        
        print(f"      - Successfully generated {len(generated_tests)} test cases from the table.")
        
        formatted_tests = []
        for test in generated_tests:
            if not isinstance(test, dict):
                print(f"      - WARNING: AI returned an invalid item (not a dictionary). Item was: '{test}'")
                continue
            
            formatted_case = self.formatter.format_test_case(test, requirement['id'], issue_id_counter)
            formatted_tests.append(formatted_case)
            issue_id_counter += 1
        
        return formatted_tests, issue_id_counter
    
    def _save_test_cases(self, master_test_list: List[Dict[str, Any]], 
                        output_path: Path, filename: str) -> None:
        """Save test cases to CSV file"""
        if master_test_list:
            print(f"\nSaving {len(master_test_list)} total test cases to '{output_path.name}'...")
            df = pd.DataFrame(master_test_list)
            
            # Use encoding from configuration if available
            encoding = getattr(self.config_manager, 'file_processing', {}).get('OUTPUT_ENCODING', 'utf-8-sig')
            df.to_csv(output_path, index=False, encoding=encoding)
            print("✅ Success!")
        else:
            print(f"\nNo test cases were generated for the entire file '{filename}'.")


# =================================================================
# COMMAND LINE INTERFACE
# =================================================================

class CommandLineInterface:
    """Handles command line argument parsing and file discovery"""
    
    @staticmethod
    def parse_arguments() -> argparse.Namespace:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="Context-Aware Granular Test Case Generator for REQIFZ files.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s input.reqifz                    # Process single file with default model
  %(prog)s /path/to/reqifz/files/          # Process all .reqifz files in directory
  %(prog)s input.reqifz --model llama3.1:8b    # Use specific model
  %(prog)s input.reqifz --model deepseek-coder-v2:16b  # Use DeepSeek model

Available Models:
  - llama3.1:8b (default)
  - deepseek-coder-v2:16b
  - Or any other Ollama model you have installed
            """
        )
        parser.add_argument(
            "input_path", 
            help="Path to a single .reqifz file or a folder of .reqifz files."
        )
        parser.add_argument(
            "--model", 
            default="llama3.1:8b", 
            help="Ollama model to use for test generation (default: %(default)s)"
        )
        parser.add_argument(
            "--config",
            help="Path to custom configuration file (optional)"
        )
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose output"
        )
        return parser.parse_args()
    
    @staticmethod
    def discover_files(input_path: Path) -> List[Path]:
        """
        Discover REQIFZ files to process
        
        Args:
            input_path: Input path (file or directory)
            
        Returns:
            List of REQIFZ file paths to process
        """
        if not input_path.exists():
            raise FileNotFoundError(f"The path '{input_path}' does not exist.")
        
        files_to_process = []
        
        if input_path.is_file():
            if input_path.suffix.lower() == '.reqifz':
                files_to_process.append(input_path)
        elif input_path.is_dir():
            files_to_process = list(input_path.rglob('*.reqifz'))
        
        if not files_to_process:
            raise ValueError("No .reqifz files found to process.")
        
        return files_to_process


# =================================================================
# APPLICATION FACTORY
# =================================================================

class ApplicationFactory:
    """Factory class for creating application components"""
    
    @staticmethod
    def create_config_manager(config_file_path: str = None) -> ConfigManager:
        """
        Create configuration manager with optional custom config file
        
        Args:
            config_file_path: Path to custom configuration file
            
        Returns:
            Configured ConfigManager instance
        """
        config_manager = ConfigManager()
        
        if config_file_path and Path(config_file_path).exists():
            try:
                import yaml
                with open(config_file_path, 'r') as f:
                    custom_config = yaml.safe_load(f)
                config_manager.update_from_dict(custom_config)
                print(f"Loaded custom configuration from: {config_file_path}")
            except Exception as e:
                print(f"Warning: Failed to load custom config file: {e}")
                print("Using default configuration.")
        
        return config_manager
    
    @staticmethod
    def create_processor(model_name: str, config_manager: ConfigManager) -> REQIFZFileProcessor:
        """
        Create file processor with given model and configuration
        
        Args:
            model_name: Name of the AI model to use
            config_manager: Configuration manager instance
            
        Returns:
            Configured REQIFZFileProcessor instance
        """
        return REQIFZFileProcessor(model_name, config_manager)


# =================================================================
# MAIN APPLICATION
# =================================================================

def print_banner():
    """Print application banner"""
    print("=" * 70)
    print("  AI Test Case Generator v1.1 (Refactored)")
    print("  Context-Rich Test Case Generation from REQIFZ Files")
    print("=" * 70)


def validate_model_availability(model_name: str) -> bool:
    """
    Validate that the specified model is available in Ollama
    
    Args:
        model_name: Name of the model to validate
        
    Returns:
        True if model is available, False otherwise
    """
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        if response.status_code == 200:
            available_models = [model['name'] for model in response.json().get('models', [])]
            return model_name in available_models
        return False
    except:
        return False


def main():
    """Main application entry point"""
    try:
        print_banner()
        
        # Parse command line arguments
        args = CommandLineInterface.parse_arguments()
        input_path = Path(args.input_path)
        
        # Validate model availability
        if not validate_model_availability(args.model):
            print(f"⚠️  Warning: Model '{args.model}' may not be available in Ollama.")
            print("   Available models can be checked with: ollama list")
            print("   Continuing anyway...")
        
        # Create configuration manager
        config_manager = ApplicationFactory.create_config_manager(args.config)
        
        # Discover files to process
        files_to_process = CommandLineInterface.discover_files(input_path)
        print(f"\n📁 Found {len(files_to_process)} .reqifz file(s) to process")
        
        # Create processor
        processor = ApplicationFactory.create_processor(args.model, config_manager)
        
        # Process each file
        for i, reqifz_file in enumerate(files_to_process, 1):
            print(f"\n[{i}/{len(files_to_process)}] Processing: {reqifz_file.name}")
            processor.process_file(reqifz_file)
        
        print(f"\n🎉 Processing complete! Generated test cases for {len(files_to_process)} file(s).")
            
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user.")
        return 1
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        if args.verbose if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


def safe_filename(text: str, max_len: int = 50) -> str:
    """
    Create a safe filename from text
    
    Args:
        text: Input text
        max_len: Maximum length of filename
        
    Returns:
        Safe filename string
    """
    text = re.sub(r'[\\/*?:"<>|]', "_", text)
    text = text.replace(' ', '_')
    return text[:max_len]


if __name__ == "__main__":
    exit(main())
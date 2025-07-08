# =================================================================
#  Context-Rich, High-Performance Test Case Generator
#  Version: Final
#
#  - FIX: Uses the exact model name 'llama3.1:8b' to match the user's system.
#  - Uses the proven v1.0 table parser for maximum coverage.
#  - Provides a full "Context Package" to the AI for superior results.
# =================================================================

import zipfile
import xml.etree.ElementTree as ET
import requests
import json
import pandas as pd
from pathlib import Path
import argparse
import re

# --- Static Configuration ---
STATIC_VOLTAGE_PRECONDITION = "1. Voltage= 12V\n2. Bat-ON"
STATIC_TEST_TYPE = "RoboFIT"
STATIC_ISSUE_TYPE = "Test"
STATIC_PROJECT_KEY = "TCTOIC"
STATIC_ASSIGNEE = "ENGG"
STATIC_PLANNED_EXECUTION = "Manual"
STATIC_TEST_CASE_TYPE = "Feature Functional"
STATIC_COMPONENTS = "FEAT"
STATIC_LABELS = "SYS_DI_VALIDATION_TEST"

# --- Core Helper Functions ---
def call_ollama(model_name, prompt, is_json=False, timeout=600):
    print(f"      - Calling model '{model_name}' (deterministic mode)...")
    api_url = "http://127.0.0.1:11434/api/generate"
    payload = {"model": model_name, "prompt": prompt, "stream": False, "options": {"temperature": 0.0}}
    if is_json: payload["format"] = "json"
    proxies = {"http": None, "https": None}
    try:
        response = requests.post(api_url, json=payload, proxies=proxies, timeout=timeout)
        response.raise_for_status()
        return json.loads(response.text).get("response", "")
    except Exception as e:
        print(f"  -> OLLAMA API ERROR with model {model_name}: {e}")
        return ""

def extract_json_from_response(response_text):
    try:
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
        return None
    except (json.JSONDecodeError, IndexError):
        return None

def parse_html_table(table_element, ns):
    headers, data_rows = [], []
    raw_rows = table_element.findall('.//html:tr', ns)
    if not raw_rows: return None
    grid = [[] for _ in range(len(raw_rows))]
    for r, tr in enumerate(raw_rows):
        for td in tr.findall('.//html:td', ns) + tr.findall('.//html:th', ns):
            c = 0
            while c < len(grid[r]): c += 1
            text = ''.join(td.itertext()).strip()
            colspan, rowspan = int(td.get('colspan', 1)), int(td.get('rowspan', 1))
            for i in range(r, r + rowspan):
                j_start = c 
                while len(grid[i]) < j_start + colspan: grid[i].append('')
                for j in range(j_start, j_start + colspan): grid[i][j] = text
    for r_idx, row in enumerate(grid):
        for c_idx, cell in enumerate(row):
            if cell == '' and r_idx > 0 and c_idx < len(grid[r_idx-1]):
                grid[r_idx][c_idx] = grid[r_idx-1][c_idx]
    if len(grid) >= 2:
        header_row1, header_row2 = grid[0], grid[1]
        data_rows = grid[2:]
        merged_headers = []
        c = 0
        while c < len(header_row1):
            span_text = header_row1[c]
            span_count = 1
            while c + span_count < len(header_row1) and header_row1[c + span_count] == span_text:
                span_count += 1
            if span_text and span_text not in ["Input", "Output", "No."]:
                 for i in range(span_count): merged_headers.append(header_row2[c+i])
            else:
                for i in range(span_count): merged_headers.append(f"{span_text} - {header_row2[c+i]}")
            c += span_count
        headers = merged_headers
    return {'headers': headers, 'rows': data_rows}

def extract_all_artifacts(file_path):
    all_objects = []
    ns = {'reqif': 'http://www.omg.org/spec/ReqIF/20110401/reqif.xsd', 'html': 'http://www.w3.org/1999/xhtml'}
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            reqif_filename = next((name for name in zf.namelist() if name.endswith('.reqif')), None)
            if not reqif_filename: raise FileNotFoundError("No .reqif file found in the archive.")
            with zf.open(reqif_filename) as reqif_file:
                tree = ET.parse(reqif_file)
                root = tree.getroot()
                type_map = { t.get('IDENTIFIER'): t.get('LONG-NAME') for t in root.findall('.//reqif:SPEC-OBJECT-TYPE', ns) }
                type_to_foreign_id_map, type_to_text_def_map = {}, {}
                for spec_type in root.findall('.//reqif:SPEC-OBJECT-TYPE', ns):
                    type_id = spec_type.get('IDENTIFIER')
                    foreign_id_def = spec_type.find(".//reqif:ATTRIBUTE-DEFINITION-STRING[@LONG-NAME='ReqIF.ForeignID']", ns)
                    if foreign_id_def is not None: type_to_foreign_id_map[type_id] = foreign_id_def.get('IDENTIFIER')
                    text_def = spec_type.find(".//reqif:ATTRIBUTE-DEFINITION-XHTML[@LONG-NAME='ReqIF.Text']", ns)
                    if text_def is not None: type_to_text_def_map[type_id] = text_def.get('IDENTIFIER')
                for spec_object in root.findall('.//reqif:SPEC-OBJECTS//reqif:SPEC-OBJECT', ns):
                    internal_id = spec_object.get('IDENTIFIER')
                    req_id, req_text, req_type, table_data = internal_id, "", "Unknown", None
                    type_ref_node = spec_object.find('reqif:TYPE/reqif:SPEC-OBJECT-TYPE-REF', ns)
                    if type_ref_node is not None:
                        spec_object_type_ref = type_ref_node.text
                        req_type = type_map.get(spec_object_type_ref, "Unknown")
                        target_foreign_id_ref = type_to_foreign_id_map.get(spec_object_type_ref)
                        target_text_def_ref = type_to_text_def_map.get(spec_object_type_ref)
                        values_container = spec_object.find('reqif:VALUES', ns)
                        if values_container is not None:
                            if target_foreign_id_ref:
                                for attr_value in values_container.findall('reqif:ATTRIBUTE-VALUE-STRING', ns):
                                    definition_ref_node = attr_value.find('reqif:DEFINITION/reqif:ATTRIBUTE-DEFINITION-STRING-REF', ns)
                                    if definition_ref_node is not None and definition_ref_node.text == target_foreign_id_ref:
                                        req_id = attr_value.get('THE-VALUE', internal_id)
                                        break
                            if target_text_def_ref:
                                for attr_value in values_container.findall('.//reqif:ATTRIBUTE-VALUE-XHTML', ns):
                                    definition_ref_node = attr_value.find('reqif:DEFINITION/reqif:ATTRIBUTE-DEFINITION-XHTML-REF', ns)
                                    if definition_ref_node is not None and definition_ref_node.text == target_text_def_ref:
                                        the_value = attr_value.find('reqif:THE-VALUE', ns)
                                        if the_value is not None:
                                            full_text = ''.join(the_value.itertext()).strip()
                                            if full_text: req_text = full_text
                                            table_element = the_value.find('.//html:table', ns)
                                            if table_element is not None: table_data = parse_html_table(table_element, ns)
                                        break
                    all_objects.append({'id': req_id, 'text': req_text.strip(), 'type': req_type, 'table': table_data})
    except Exception as e:
        print(f"  -> ERROR processing XML in '{file_path.name}': {e}")
    return all_objects

def generate_tests_with_context(requirement, heading, info_list, interface_list):
    print(f"      - Writing test cases for '{requirement['id']}' with Llama 3.1...")
    table = requirement.get('table')
    if not table: return []
    table_str = "Headers: " + ", ".join(table['headers']) + "\n"
    for i, row in enumerate(table['rows']):
        table_str += f"Row {i+1}: {row}\n"
    interface_str = "\n".join([f"- {i['id']}: {i['text']}" for i in interface_list])
    info_str = "\n".join([f"- {i['text']}" for i in info_list])
    prompt = f"""
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
    1.  Create one test case for EACH data row in the table. Ensure all {len(table['rows'])} rows are covered.
    2.  Use the context to understand terms. For example, use the System Interface Dictionary to understand what a signal like 'B_FWMSIG' means.
    3.  The `"summary_suffix"` for each test case must be a short, descriptive title for that specific test row.
    4.  The `"action"` must always be "{STATIC_VOLTAGE_PRECONDITION.replace("\n", "\\n")}".
    5.  The `"data"` must be a numbered list of all the "Input" column values for that row, formatted like "1) Set [Header Name] = [Value]".
    6.  The `"expected_result"` must be a concise statement combining all "Output" column values for that row, formatted as "Verify [Header Name] = [Value]".
    7.  Your entire response MUST be a single, valid JSON object with a single key: `"test_cases"`.
    """
    # ### THIS IS THE FIX ###
    # Use the correct model name that matches the 'deepseek-coder-v2 list' output on your system.
    response_str = call_ollama("deepseek-coder-v2", prompt, is_json=True)
    # ######################
    parsed_json = extract_json_from_response(response_str)
    return parsed_json.get("test_cases", []) if parsed_json else []

def main():
    parser = argparse.ArgumentParser(description="Context-Aware Granular Test Case Generator for REQIFZ files.")
    parser.add_argument("input_path", help="Path to a single .reqifz file or a folder of .reqifz files.")
    args = parser.parse_args()
    input_path = Path(args.input_path)
    if not input_path.exists():
        print(f"Error: The path '{input_path}' does not exist.")
        return
    files_to_process = []
    if input_path.is_file():
        if input_path.suffix.lower() == '.reqifz': files_to_process.append(input_path)
    elif input_path.is_dir():
        files_to_process = list(input_path.rglob('*.reqifz'))
    if not files_to_process:
        print("No .reqifz files found to process.")
        return
    for reqifz_file in files_to_process:
        print(f"\n===== Processing File: {reqifz_file.name} =====")
        output_csv_path = reqifz_file.with_name(f"{reqifz_file.stem}_TCD_deepseek-coder-v2_Final.csv")
        all_objects = extract_all_artifacts(reqifz_file)
        if not all_objects:
            print("  -> No objects found in the file. Skipping.")
            continue
        system_interfaces = [obj for obj in all_objects if obj['type'] == 'System Interface']
        processing_list = [obj for obj in all_objects if obj['type'] != 'System Interface']
        print(f"  -> Found {len(system_interfaces)} 'System Interface' definitions to use as a global dictionary.")
        master_test_list, issue_id_counter, current_heading, info_since_heading = [], 1, "No Heading", []
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
                print(f"  --- Analyzing Requirement {i+1}/{len(processing_list)} (ID: {obj['id']}) ---")
                generated_tests = generate_tests_with_context(obj, current_heading, info_since_heading, system_interfaces)
                if not generated_tests:
                    print(f"      - AI failed to generate test cases for this table.")
                    continue
                print(f"      - Successfully generated {len(generated_tests)} test cases from the table.")
                for test in generated_tests:
                    if not isinstance(test, dict):
                        print(f"      - WARNING: AI returned an invalid item (not a dictionary). Item was: '{test}'")
                        continue
                    formatted_case = {
                        'Issue ID': issue_id_counter, 'Summary': f"[{obj['id']}] {test.get('summary_suffix', 'Generated Test')}",
                        'Test Type': STATIC_TEST_TYPE, 'Issue Type': STATIC_ISSUE_TYPE, 'Project Key': STATIC_PROJECT_KEY, 'Assignee': STATIC_ASSIGNEE,
                        'Description': '', 'Action': test.get('action', STATIC_VOLTAGE_PRECONDITION),
                        'Data': test.get('data', 'N/A'), 'Expected Result': test.get('expected_result', 'N/A'),
                        'Planned Execution': STATIC_PLANNED_EXECUTION, 'Test Case Type': STATIC_TEST_CASE_TYPE,
                        'Components': STATIC_COMPONENTS, 'Labels': STATIC_LABELS, 'LinkTest': obj['id']
                    }
                    master_test_list.append(formatted_case)
                    issue_id_counter += 1
                info_since_heading = []
        if master_test_list:
            print(f"\nSaving {len(master_test_list)} total test cases to '{output_csv_path.name}'...")
            df = pd.DataFrame(master_test_list)
            df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
            print("✅ Success!")
        else:
            print(f"\nNo test cases were generated for the entire file '{reqifz_file.name}'.")

def safe_filename(text, max_len=50):
    text = re.sub(r'[\\/*?:"<>|]', "_", text)
    text = text.replace(' ', '_')
    return text[:max_len]

if __name__ == "__main__":
    main()
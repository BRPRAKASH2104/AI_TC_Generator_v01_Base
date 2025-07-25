python test_gen_arg.py "C:\Auto_Generate\ACC.reqifz"


// To Generate the Requirement IDs alone in a csv file. //
python extract_reqids.py "C:\Auto_Generate\ACC.reqifz"
or
python extract_reqids.py "D:\My_Project_Requirements"


// Internal_IDENTIFIER: Containing the long, system-generated ID (e.g., _a1b2c3d4-e5f6...).//
// Human_Readable_ID: Containing the short, human-friendly ID (e.g., SW-REQ-123).          //

python map_reqids.py "C:\Auto_Generate\ACC.reqifz"
or
python map_reqids.py "D:\My_Project_Requirements"

// Granular TC Generation //
python generate_granular_tcs.py "..\reqifz_files"




APPROACH #2
===========
//Verify Ollama Installation
ollama --version

// Download and Run Your AI Model
ollama run llama3:8b
ollama run mistral

// Confirm the Model is Available
ollama list

// Create a Python Virtual Environment
python -m venv venv

// Activate the Virtual Environment
.\venv\Scripts\activate

// Install required plugins
pip install pandas requests

// Run the Script - to parse the requirements
python Src\parse_reqifz.py

// Run the Script - to tag the requirements (make your requirements machine-readable and searchable)
python Src\tag_requirements.py

// Run the Script - Instruct the local AI to brainstorm test scenarios in the human-readable Gherkin format (Given-When-Then)
python Src\generate_test_ideas.py

// AI Test Case Generation into CSV Format
python Src\generate_test_cases.py

// Below command will orchestrate the two models to achieve more comprehensive and detailed test case generation.
python Src\generate_test_cases_collaborative.py
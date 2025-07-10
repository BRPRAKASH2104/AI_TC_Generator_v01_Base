#!/usr/bin/env python3
"""
Simple script to create a mock .reqifz file for testing
"""

import zipfile
import os

# Create the REQIF XML content as a string
REQIF_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:html="http://www.w3.org/1999/xhtml">
  <THE-HEADER>
    <REQ-IF-HEADER IDENTIFIER="header-001" CREATION-TIME="2025-01-15T10:00:00" REQ-IF-TOOL-ID="MockGenerator" REQ-IF-VERSION="1.0" SOURCE-TOOL-ID="TestTool"/>
  </THE-HEADER>
  
  <CORE-CONTENT>
    <REQ-IF-CONTENT>
      
      <!-- Data Types -->
      <DATATYPES>
        <DATATYPE-DEFINITION-STRING IDENTIFIER="string-type-001" LONG-NAME="String Type" MAX-LENGTH="1000"/>
        <DATATYPE-DEFINITION-XHTML IDENTIFIER="xhtml-type-001" LONG-NAME="XHTML Type"/>
      </DATATYPES>
      
      <!-- Spec Types -->
      <SPEC-TYPES>
        <!-- Heading Type -->
        <SPEC-OBJECT-TYPE IDENTIFIER="heading-type-001" LONG-NAME="Heading">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="heading-foreign-id" LONG-NAME="ReqIF.ForeignID">
              <TYPE><DATATYPE-DEFINITION-STRING-REF>string-type-001</DATATYPE-DEFINITION-STRING-REF></TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
            <ATTRIBUTE-DEFINITION-XHTML IDENTIFIER="heading-text" LONG-NAME="ReqIF.Text">
              <TYPE><DATATYPE-DEFINITION-XHTML-REF>xhtml-type-001</DATATYPE-DEFINITION-XHTML-REF></TYPE>
            </ATTRIBUTE-DEFINITION-XHTML>
          </SPEC-ATTRIBUTES>
        </SPEC-OBJECT-TYPE>
        
        <!-- Information Type -->
        <SPEC-OBJECT-TYPE IDENTIFIER="info-type-001" LONG-NAME="Information">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="info-foreign-id" LONG-NAME="ReqIF.ForeignID">
              <TYPE><DATATYPE-DEFINITION-STRING-REF>string-type-001</DATATYPE-DEFINITION-STRING-REF></TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
            <ATTRIBUTE-DEFINITION-XHTML IDENTIFIER="info-text" LONG-NAME="ReqIF.Text">
              <TYPE><DATATYPE-DEFINITION-XHTML-REF>xhtml-type-001</DATATYPE-DEFINITION-XHTML-REF></TYPE>
            </ATTRIBUTE-DEFINITION-XHTML>
          </SPEC-ATTRIBUTES>
        </SPEC-OBJECT-TYPE>
        
        <!-- System Requirements Type -->
        <SPEC-OBJECT-TYPE IDENTIFIER="req-type-001" LONG-NAME="System Requirements">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="req-foreign-id" LONG-NAME="ReqIF.ForeignID">
              <TYPE><DATATYPE-DEFINITION-STRING-REF>string-type-001</DATATYPE-DEFINITION-STRING-REF></TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
            <ATTRIBUTE-DEFINITION-XHTML IDENTIFIER="req-text" LONG-NAME="ReqIF.Text">
              <TYPE><DATATYPE-DEFINITION-XHTML-REF>xhtml-type-001</DATATYPE-DEFINITION-XHTML-REF></TYPE>
            </ATTRIBUTE-DEFINITION-XHTML>
          </SPEC-ATTRIBUTES>
        </SPEC-OBJECT-TYPE>
        
        <!-- System Interface Type -->
        <SPEC-OBJECT-TYPE IDENTIFIER="interface-type-001" LONG-NAME="System Interface">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="interface-foreign-id" LONG-NAME="ReqIF.ForeignID">
              <TYPE><DATATYPE-DEFINITION-STRING-REF>string-type-001</DATATYPE-DEFINITION-STRING-REF></TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
            <ATTRIBUTE-DEFINITION-XHTML IDENTIFIER="interface-text" LONG-NAME="ReqIF.Text">
              <TYPE><DATATYPE-DEFINITION-XHTML-REF>xhtml-type-001</DATATYPE-DEFINITION-XHTML-REF></TYPE>
            </ATTRIBUTE-DEFINITION-XHTML>
          </SPEC-ATTRIBUTES>
        </SPEC-OBJECT-TYPE>

        <!-- Design Information Type -->
        <SPEC-OBJECT-TYPE IDENTIFIER="design-type-001" LONG-NAME="Design Information">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="design-foreign-id" LONG-NAME="ReqIF.ForeignID">
              <TYPE><DATATYPE-DEFINITION-STRING-REF>string-type-001</DATATYPE-DEFINITION-STRING-REF></TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
            <ATTRIBUTE-DEFINITION-XHTML IDENTIFIER="design-text" LONG-NAME="ReqIF.Text">
              <TYPE><DATATYPE-DEFINITION-XHTML-REF>xhtml-type-001</DATATYPE-DEFINITION-XHTML-REF></TYPE>
            </ATTRIBUTE-DEFINITION-XHTML>
          </SPEC-ATTRIBUTES>
        </SPEC-OBJECT-TYPE>

        <!-- Application Parameter Type -->
        <SPEC-OBJECT-TYPE IDENTIFIER="param-type-001" LONG-NAME="Application Parameter">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="param-foreign-id" LONG-NAME="ReqIF.ForeignID">
              <TYPE><DATATYPE-DEFINITION-STRING-REF>string-type-001</DATATYPE-DEFINITION-STRING-REF></TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
            <ATTRIBUTE-DEFINITION-XHTML IDENTIFIER="param-text" LONG-NAME="ReqIF.Text">
              <TYPE><DATATYPE-DEFINITION-XHTML-REF>xhtml-type-001</DATATYPE-DEFINITION-XHTML-REF></TYPE>
            </ATTRIBUTE-DEFINITION-XHTML>
          </SPEC-ATTRIBUTES>
        </SPEC-OBJECT-TYPE>
      </SPEC-TYPES>
      
      <!-- Spec Objects -->
      <SPEC-OBJECTS>
        
        <!-- Heading 1: Door Control System -->
        <SPEC-OBJECT IDENTIFIER="obj-001">
          <TYPE><SPEC-OBJECT-TYPE-REF>heading-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="HEAD_DCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>heading-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>heading-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>Door Control System - Safety and Security Features</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- Information about door control -->
        <SPEC-OBJECT IDENTIFIER="obj-002">
          <TYPE><SPEC-OBJECT-TYPE-REF>info-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="INFO_DCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>info-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>info-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>The door control system manages automatic locking and unlocking based on vehicle motion, speed, and door state. This system is critical for passenger safety and vehicle security.</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>

        <!-- Design Information -->
        <SPEC-OBJECT IDENTIFIER="obj-003">
          <TYPE><SPEC-OBJECT-TYPE-REF>design-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="DESIGN_DCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>design-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>design-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>Door Control ECU Architecture: The system receives inputs from CAN bus (vehicle speed, gear position), door sensors (open/close state), and motion sensors. Primary output controls the door lock actuators via relay drivers.</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>

        <!-- Application Parameter 1 -->
        <SPEC-OBJECT IDENTIFIER="obj-004">
          <TYPE><SPEC-OBJECT-TYPE-REF>param-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="PARAM_DCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>param-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>param-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>SPEED_THRESHOLD: 5 km/h - Minimum vehicle speed required for automatic door locking activation</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>

        <!-- System Interface 1 -->
        <SPEC-OBJECT IDENTIFIER="obj-005">
          <TYPE><SPEC-OBJECT-TYPE-REF>interface-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="SIF_DCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>interface-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>interface-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>B_VEHICLE_MOVING: Boolean input signal from vehicle motion sensor indicating forward/reverse movement</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- System Interface 2 -->
        <SPEC-OBJECT IDENTIFIER="obj-006">
          <TYPE><SPEC-OBJECT-TYPE-REF>interface-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="SIF_DCS_002">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>interface-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>interface-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>B_DOOR_OPEN: Boolean input signal from door position sensor (0=closed, 1=open)</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- System Interface 3 -->
        <SPEC-OBJECT IDENTIFIER="obj-007">
          <TYPE><SPEC-OBJECT-TYPE-REF>interface-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="SIF_DCS_003">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>interface-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>interface-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>B_SPEED_ABOVE_THRESHOLD: Boolean input signal indicating vehicle speed > 5 km/h</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- System Interface 4 -->
        <SPEC-OBJECT IDENTIFIER="obj-008">
          <TYPE><SPEC-OBJECT-TYPE-REF>interface-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="SIF_DCS_004">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>interface-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>interface-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>B_DOOR_LOCK_CMD: Boolean output command to door lock actuator (1=lock, 0=unlock)</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- System Requirement with Table -->
        <SPEC-OBJECT IDENTIFIER="obj-009">
          <TYPE><SPEC-OBJECT-TYPE-REF>req-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="REQ_DCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>req-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>req-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE>
                <html:div>
                  <html:p>Automatic Door Lock Control Logic</html:p>
                  <html:table border="1">
                    <html:tr>
                      <html:th colspan="1">No.</html:th>
                      <html:th colspan="3">Input</html:th>
                      <html:th colspan="1">Output</html:th>
                    </html:tr>
                    <html:tr>
                      <html:th>Test Case</html:th>
                      <html:th>B_VEHICLE_MOVING</html:th>
                      <html:th>B_DOOR_OPEN</html:th>
                      <html:th>B_SPEED_ABOVE_THRESHOLD</html:th>
                      <html:th>B_DOOR_LOCK_CMD</html:th>
                    </html:tr>
                    <html:tr>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>2</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>3</html:td>
                      <html:td>0</html:td>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>4</html:td>
                      <html:td>0</html:td>
                      <html:td>1</html:td>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>5</html:td>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>6</html:td>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                      <html:td>1</html:td>
                      <html:td>1</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>7</html:td>
                      <html:td>1</html:td>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>8</html:td>
                      <html:td>1</html:td>
                      <html:td>1</html:td>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                    </html:tr>
                  </html:table>
                </html:div>
              </THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- Heading 2: Window Control System -->
        <SPEC-OBJECT IDENTIFIER="obj-010">
          <TYPE><SPEC-OBJECT-TYPE-REF>heading-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="HEAD_WCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>heading-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>heading-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>Window Control System - Automatic Rain Response</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>

        <!-- System Interface 5 -->
        <SPEC-OBJECT IDENTIFIER="obj-011">
          <TYPE><SPEC-OBJECT-TYPE-REF>interface-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="SIF_WCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>interface-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>interface-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>B_MANUAL_WINDOW_UP: Boolean input from driver window up switch</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- System Interface 6 -->
        <SPEC-OBJECT IDENTIFIER="obj-012">
          <TYPE><SPEC-OBJECT-TYPE-REF>interface-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="SIF_WCS_002">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>interface-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>interface-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>B_RAIN_DETECTED: Boolean input signal from rain sensor (1=rain detected, 0=no rain)</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- System Interface 7 -->
        <SPEC-OBJECT IDENTIFIER="obj-013">
          <TYPE><SPEC-OBJECT-TYPE-REF>interface-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="SIF_WCS_003">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>interface-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>interface-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE><html:p>B_WINDOW_MOTOR_UP: Boolean output command to window motor for upward movement</html:p></THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
        <!-- System Requirement with Table 2 -->
        <SPEC-OBJECT IDENTIFIER="obj-014">
          <TYPE><SPEC-OBJECT-TYPE-REF>req-type-001</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES>
            <ATTRIBUTE-VALUE-STRING THE-VALUE="REQ_WCS_001">
              <DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>req-foreign-id</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>req-text</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
              <THE-VALUE>
                <html:div>
                  <html:p>Automatic Window Control with Rain Override Logic</html:p>
                  <html:table border="1">
                    <html:tr>
                      <html:th colspan="1">No.</html:th>
                      <html:th colspan="2">Input</html:th>
                      <html:th colspan="1">Output</html:th>
                    </html:tr>
                    <html:tr>
                      <html:th>Test Case</html:th>
                      <html:th>B_MANUAL_WINDOW_UP</html:th>
                      <html:th>B_RAIN_DETECTED</html:th>
                      <html:th>B_WINDOW_MOTOR_UP</html:th>
                    </html:tr>
                    <html:tr>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                      <html:td>0</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>2</html:td>
                      <html:td>0</html:td>
                      <html:td>1</html:td>
                      <html:td>1</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>3</html:td>
                      <html:td>1</html:td>
                      <html:td>0</html:td>
                      <html:td>1</html:td>
                    </html:tr>
                    <html:tr>
                      <html:td>4</html:td>
                      <html:td>1</html:td>
                      <html:td>1</html:td>
                      <html:td>1</html:td>
                    </html:tr>
                  </html:table>
                </html:div>
              </THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
        </SPEC-OBJECT>
        
      </SPEC-OBJECTS>
    </REQ-IF-CONTENT>
  </CORE-CONTENT>
</REQ-IF>'''

def create_reqifz_file():
    """Create the .reqifz file"""
    
    # Step 1: Write the REQIF XML to a temporary file
    reqif_filename = "automotive_door_window_system.reqif"
    
    with open(reqif_filename, 'w', encoding='utf-8') as f:
        f.write(REQIF_XML)
    
    # Step 2: Create the .reqifz (ZIP) file
    reqifz_filename = "automotive_door_window_system.reqifz"
    
    with zipfile.ZipFile(reqifz_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(reqif_filename)
    
    # Step 3: Clean up the temporary .reqif file
    if os.path.exists(reqif_filename):
        os.remove(reqif_filename)
    
    return reqifz_filename

if __name__ == "__main__":
    print("🚗 Creating Mock Automotive REQIFZ File...")
    print("📋 Following artifact types from JIRA_Requirement_Artifact_Types.txt")
    print()
    
    filename = create_reqifz_file()
    
    print(f"✅ Created: {filename}")
    print()
    print("📊 Content Summary:")
    print("  • 2 Headings (Door Control, Window Control)")
    print("  • 1 Information block (contextual notes)")
    print("  • 1 Design Information (system architecture)")
    print("  • 1 Application Parameter (speed threshold)")
    print("  • 7 System Interface definitions (inputs/outputs)")
    print("  • 2 System Requirements with test tables")
    print("  • 12 total test cases across both tables")
    print()
    print("🎯 Test Cases Include:")
    print("  Door Control: 8 test cases covering vehicle motion, door state, speed, and locking logic")
    print("  Window Control: 4 test cases covering manual control and rain detection")
    print()
    print("✅ Ready for testing with your AI TC Generator!")
    print("💡 This file follows the exact artifact types defined in your project!")
    print()
    print("📝 Usage:")
    print(f"  python src/generate_contextual_tests_Llama31_v1.0.py {filename}")
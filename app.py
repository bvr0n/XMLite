from flask import Flask, render_template, request, redirect, flash, url_for
import xmlschema , lxml ,  json , xmltodict
from lxml import etree 
from xmlschema import XMLSchema
from xml.dom import minidom
import lxml.etree as ET
from xml.etree.ElementTree import parse
import subprocess

app = Flask(__name__)


#************************************** function traits internal DTD ***************************************************
def InternalDTD(varDTD):
    try:
        tree = etree.parse(varDTD)
        dtd = tree.docinfo.internalDTD
        root = tree.getroot()
        is_valid = dtd.assertValid(root)
        msg = True

    except lxml.etree.DocumentInvalid as valide:
        msg =  valide
    return(msg)
#***********************************************************************************************************************

#******************************************* Routes for the MENU********************************************************
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/xmlschema')
def xsd():
    return render_template('xmlschema.html')

@app.route('/intdtd')
def intdtd():
    return render_template('intdtd.html')

@app.route('/extdtd')
def extdtd():
    return render_template('extdtd.html')

@app.route('/xmltojson')
def xmljson():
    return render_template('xmltojson.html')

@app.route('/dtdtoxsd')
def dtdxsd():
    return render_template('dtdtoxsd.html')
#***********************************************************************************************************************

#************************************************** DTD Part ***********************************************************
#*************************EXTERNAL DTD****************************
#**VALIDETE XML USING EXTERNAL DTD TEXTAREA***
@app.route('/DTD_TEXT', methods=['POST'])
def input_dtd():
    input_file1 = request.form['xml1']
    text_file1 = open("xxxDTD.xml", "w")
    text_file1.write(input_file1)
    text_file1.close()
    input_file2 = request.form['dtd1']
    text_file2 = open("xxxDTD.xsd", "w")
    text_file2.write(input_file2)
    text_file2.close()
    try:
        xml_file = lxml.etree.parse("xxxDTD.xml")
        xml_validator = lxml.etree.DTD(file="xxxDTD.xsd")
        valide = xml_validator.assertValid(xml_file)
        mes = True
    except lxml.etree.DocumentInvalid as valide:
        mes=valide
    return render_template('extdtd.html', message4=mes)
#**VALIDATE XML USING EXTERNAL DTD FILES**
@app.route('/extdtd', methods=['POST'])
def exdtdfile():
    if request.method == 'POST':
        f1 = request.files['f1']
        f2 = request.files['f2']
        f1.save(f1.filename)
        f2.save(f2.filename)
    try:
        dtd = lxml.etree.DTD(f1.filename)
        tree = lxml.etree.parse(f2.filename)
        valide = dtd.assertValid(tree)
        mes = True
    except lxml.etree.DocumentInvalid as valide:
        mes=valide
    return render_template('extdtd.html', message6=mes)
#*************************INTERNAL DTD****************************
#**VALIDATE XML USING INTERNAL DTD (FILE)**
@app.route('/intdtd', methods=['POST'])
def upload_file2():
    uploaded_file1 = request.files['file3']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)

    valide = InternalDTD(uploaded_file1.filename)
    return render_template('intdtd.html', message1=valide)


#**VALIDATE XML USING INTERNAL DTD TEXTAREA**
@app.route('/xml_DTD_TEXT', methods=['POST'])
def upload_file5():
    input_file1 = request.form['Xml_Dtd']
    text_file1 = open("xxxXmlDtd.xml", "w")
    text_file1.write(input_file1)
    text_file1.close()
    valide = InternalDTD("xxxXmlDtd.xml")
    return render_template('intdtd.html', message5=valide)
#***********************************************************************************************************************

#***************************************** VALIDATE XML USING XMLSCHEMA ************************************************
#********** USING FILES XMLSCHEMA*********
@app.route('/xmlschema', methods=['POST'])
def upload_file():
    uploaded_file1 = request.files['file1']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)

    uploaded_file2 = request.files['file2']
    if uploaded_file2.filename != '':
        uploaded_file2.save(uploaded_file2.filename)


    try:
        xml_file = lxml.etree.parse(uploaded_file1.filename)
        xml_validator = lxml.etree.XMLSchema(file=uploaded_file2.filename)

        is_valid = xml_validator.assertValid(xml_file)

    except Exception as valide:
        return render_template('xmlschema.html', message=valide)
    return render_template('xmlschema.html', message=True)

#********  USING TEXTAREA XMLSCHEMA********
@app.route('/XSD', methods=['POST'])
def input_xsd():
    input_file1 = request.form['xml']
    text_file1 = open("TextArea.xml", "w")
    text_file1.write(input_file1)
    text_file1.close()

    input_file2 = request.form['xsd']
    text_file2 = open("TextArea.xsd", "w")
    text_file2.write(input_file2)
    text_file2.close()

    try:
        xml_file = lxml.etree.parse("TextArea.xml")
        xml_validator = lxml.etree.XMLSchema(file="TextArea.xsd")

        is_valid = xml_validator.assertValid(xml_file)
    except Exception as valide:
        return render_template('xmlschema.html', message3=valide)

    return render_template('xmlschema.html', message3=True)



  # *****************************************  XML to json  ************************************************
    # ********** USING FILES xml*********
@app.route('/xmltojson', methods=['GET', 'POST'])
def uploadd_file():
    uploaded_file1 = request.files['file1']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)

    with open(uploaded_file1.filename) as fd:
        doc = xmltodict.parse(fd.read())


    return render_template('xmltojson.html', message3=json.dumps(doc, indent=4, separators=(". ", " = ")))



  # *****************************************  DTD to XSD  ************************************************
    # ********** USING FILES XMLSCHEMA*********
@app.route('/dtdtoxsd', methods=['GET', 'POST'])
def uploaddd_file():
    uploaded_file1 = request.files['file1']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)
   
    # DTD to convert
    with open(uploaded_file1.filename, 'r') as file:
    # Read the contents of the file
        dtd = file.read()    
    i=0
    # Initialize XSD string
    xsd = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
    child_element=""
    element_name=""
    list=[]
    # Split DTD into lines
    lines = dtd.strip().split("\n")
    # Loop through lines of DTD
    for line in lines:
        # Check if line is element declaration
        
        if line.startswith("<!ELEMENT"):
            # Split line into parts
            parts = line.split()
            # Get element name and content model
            element_name = parts[1]

            element_content = parts[2]
            # Check if content model is list of elements
            if element_content.startswith("(#"):
                # Extract list of element names
                if (element_name not in list ):
                # Generate XSD syntax for simple type
                    xsd += f"""
    <xs:element name="{element_name}" type="xs:string"/>
    """
            else :
                element_content = element_content[1:-1]
                element_list = element_content.split(",")
                # Generate XSD syntax for complex type with sequence of elements
                xsd += f"""
    <xs:element name="{element_name}" type="{element_name}Type">
    </xs:element>
    <xs:complexType name="{element_name}Type">
        <xs:sequence>
    """
                # Add element declaration for each element in list
                for child_element in element_list:
                    child_element = child_element.strip()
                    list.insert(i, child_element)

                    i=i+1
                    xsd += f"""
        <xs:element name="{child_element}" type="xs:string"/>
    """
                xsd += """
        </xs:sequence>
    </xs:complexType>
    """
            # If content model is not list of elements, it must be simple type

        # Check if line is attribute list declaration
        elif line.startswith("<!ATTLIST"):
            # Split line into parts
            parts = line.split()
            # Get element name and attribute name
            element_name = parts[1]
            attribute_name = parts[2]
            # Get attribute type
            attribute_type = parts[3]
            # Check if attribute type is enumeration
            if attribute_type.startswith("("):
                # Extract list of enumeration values
                attribute_type = attribute_type[1:-1]
                enumeration_values = attribute_type.split("|")
                # Generate XSD syntax for simple type with enumeration
                xsd += f"""
            <xs:simpleType name="{attribute_name}Type">
                <xs:restriction base="xs:string">
            """
                # Add enumeration value for each value in list
                for value in enumeration_values:
                    value = value.strip()
                    xsd += f"""
                    <xs:enumeration value="{value}"/>
            """
                xsd += """
                </xs:restriction>
            </xs:simpleType>
            """
                # Generate XSD syntax for attribute with simple type
                xsd += f"""
            <xs:attribute name="{attribute_name}" type="{attribute_name}Type"/>
            """
            # If attribute type is not enumeration, it must be simple type
            else:
                # Generate XSD syntax for attribute with simple type
                xsd += f"""
            <xs:attribute name="{attribute_name}" type="xs:String"/>
            """

    return render_template('dtdtoxsd.html', message3=xsd)

if __name__ == '__main__':
    app.run(debug=True)
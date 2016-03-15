# -*- coding: utf-8 -*-
from xml_parser.XMLParserException import XMLParserException

import re
from xml.dom import minidom

from lxml import etree

__author__ = 'xiaolong'


class XMLParser:
    """
    This class is a XML parser which can validate XML files against an XML schema definition.
    """
    XML_DECLARATION = '<?xml version="1.0" encoding="utf-8" ?>\n\n'

    def __init__(self):
        pass

    def validate_file(self, xsd_file_path="log_schema.xsd", xml_file_path="log.xml"):
        # print('validating XML file ...')

        # create a schema document by parsing the content of the xsd file
        xml_schema_document = etree.parse(xsd_file_path)

        # create a schema using the schema document
        xmlschema = etree.XMLSchema(xml_schema_document)

        # create a xml document by parsing the content of the xml file
        xml_document = etree.parse(xml_file_path)

        # try to validate the file
        return xmlschema.validate(xml_document)

    def validate_tree(self, xsd_file_path, xml_tree):
        # print('validating XML tree ...')
        # create a schema document by parsing the content of the xsd file
        xml_schema_document = etree.parse(xsd_file_path)
        # create a schema using the schema document
        xmlschema = etree.XMLSchema(xml_schema_document)

        return xmlschema.validate(xml_tree)

    def get_xml_element_tree_root(self, xsd_file_path, xml_file_path):
        if self.validate_file(xsd_file_path=xsd_file_path, xml_file_path=xml_file_path):
            with open(xml_file_path, 'r') as f:
                file_content = f.read()

                if file_content.startswith("<?"):
                    file_content = re.sub("^\<\?.*?\?\>", '', file_content, flags=re.DOTALL)

                return etree.XML(file_content)
        else:
            raise XMLParserException("XML file invalid!")

    def write_xml_file(self, xml_file_path, xml_root_element, xml_declaration=False):
        with open(xml_file_path, mode='wb') as file:
            rough_string = etree.tostring(xml_root_element, encoding='unicode', xml_declaration=xml_declaration)
            reparsed = minidom.parseString(rough_string)
            pretty_printed = reparsed.toprettyxml(indent='\t', encoding='utf-8')

            file.write(pretty_printed)

'''
Generate a query + terms set
'''

import os
import sys
import xml.etree.ElementTree as ET

def handle_xml_file(engine_xml_file):

	tree = ET.parse(engine_xml_file)
	samples = tree.getroot()

	for search_result in samples:
		for child in search_result:
			if child.tag == 'query':
				print child.attrib['id'], child.text

if __name__ == '__main__':
	engine_xml_file = sys.argv[1]

	handle_xml_file(engine_xml_file)
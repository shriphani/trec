'''
Read a snippets file and generate a trec format file
'''
import os
import sys
import xml.etree.ElementTree as ET

DOC_TEMPLATE = \
'''
<DOC>
<DOCNO> INSERT_DOCNO_HERE </DOCNO>
<TEXT>
INSERT_TEXT_HERE
</TEXT>
</DOC>
'''

OUT_DIR = '/bos/tmp17/spalakod/trec/fw13_snippets/'

def handle_xml_file(engine_xml_file):
	out_file = os.path.join(OUT_DIR, engine_xml_file.split('/')[-1] + '.trec')

	with open(out_file, 'w') as out_handle:

		tree = ET.parse(engine_xml_file)
		samples = tree.getroot()

		for search_results in samples:
			for child in search_results:
				if child.tag != 'snippets':
					continue

				for snippet in child:
					snippet_text = ''

					for snippet_child in snippet:
						if snippet_child.tag != 'title' and snippet_child.tag != 'description':
							continue
						snippet_text += unicode(snippet_child.text)

					out_handle.write(
						DOC_TEMPLATE.replace(
							'INSERT_DOCNO_HERE',
							snippet.attrib['id']
						).replace(
							'INSERT_TEXT_HERE',
							snippet_text
						)
					)

if __name__ == '__main__':
	engine_xml_file = sys.argv[1]

	# reload sys since ascii is not sufficient for fedweb
	reload(sys)
	sys.setdefaultencoding("utf-8")

	handle_xml_file(engine_xml_file)
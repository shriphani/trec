'''
Generate parameter files for building indices
'''
import os

FW14_INDICES_LOC = '/bos/tmp17/spalakod/trec/fw13_snippets_index/'

FW14_SAMPLE_DOCS_LOC = '/bos/tmp17/spalakod/trec/fw13_snippets/'

PARAMETER_FILE_TEMPLATE_LOC = 'parameter_file_template_snippets'
PARAMETER_FILE_TEMPLATE = None

if __name__ == '__main__':
	
	with open(PARAMETER_FILE_TEMPLATE_LOC, 'r') as f:
		PARAMETER_FILE_TEMPLATE = f.read()

	for engine_dir in os.listdir(FW14_SAMPLE_DOCS_LOC):
		engine_corpus_loc = os.path.join(FW14_SAMPLE_DOCS_LOC, engine_dir)
		engine_index_loc = os.path.join(FW14_INDICES_LOC, engine_dir)

		param_file = engine_dir + '.parameter'

		param_file_content = PARAMETER_FILE_TEMPLATE.replace(
			'INDEX_LOCATION', 
			engine_index_loc
		).replace(
			'CORPUS_LOCATION',
			engine_corpus_loc
		)

		with open(param_file, 'w+') as param_handle:
			param_handle.write(param_file_content)

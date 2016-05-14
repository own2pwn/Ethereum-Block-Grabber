import os
import re
import json

block_files_path = 'block_files'
max_block_number = 10000

block_numbers_statuses = [False] * max_block_number
json_file_ext_expr = re.compile('^.*\.json$')

# update block statuses (True = have valid .json file for them in block_files_path, False = missing)
for filename in os.listdir(block_files_path):
	if(json_file_ext_expr.match(filename)):
		with open(block_files_path + os.sep + filename, 'r') as blockfile:
		    try:
		    	blockdata = json.loads(blockfile.read())

		    	if(blockdata['number'] < max_block_number):
		    		block_numbers_statuses[blockdata['number']] = True;

		    except UnicodeDecodeError as ude:
		        None

# show missing
missing_blocks = list()
missing_blocks_streak = list()
for i in range(len(block_numbers_statuses)):
	if not block_numbers_statuses[i]:
		streak_broken = False
		if len(missing_blocks_streak) > 0:
			streak_broken = (missing_blocks_streak[-1] != i - 1)


		# is streak broken -> 
			#	add the streak list to missing blocks and clear the streak list
		if streak_broken:
			if len(missing_blocks_streak) < 2:
				missing_blocks.append(i)
			else:
				missing_blocks.append({'start': missing_blocks_streak[0], 'end': missing_blocks_streak[-1]+1})
			missing_blocks_streak = list()
			
		missing_blocks_streak.append(i)

# write remaining missing block numbers in streak list
if len(missing_blocks_streak) < 2:
	missing_blocks.append(i)
else:
	missing_blocks.append({'start': missing_blocks_streak[0], 'end': missing_blocks_streak[-1]+1})

# write config file with the missing blocks
config_obj = {}
config_obj['blocks'] = missing_blocks

result_config_file = open('config.json', 'w')
result_config_file.write(json.dumps(config_obj, sort_keys=True, indent=4, separators=(',', ': ')))
result_config_file.close()


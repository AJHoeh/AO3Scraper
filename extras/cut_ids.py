import csv
import os
import argparse

def get_args():
	parser = argparse.ArgumentParser(description='Removes ids before/after certain id.')
	parser.add_argument(
		'id_csv', metavar='csv',
		help='The name of the csv with the ids.')

	parser.add_argument(
		'out_csv', metavar='out_csv',
		help='The name of the csv to write the cut file to.')

	parser.add_argument(
		'first_id', metavar='first_id',
		help='The first id you want to keep.',
		default=None
	)

	parser.add_argument(
		'last_id', metavar='last_id',
		help='The last id you want to keep.',
		default=None
	)

	args = parser.parse_args()

	return args


def compare_id(id, first, last, should_copy):
	if id is first:
		return True
	elif id is last:
		return "last"
	else:
		return should_copy


if __name__ == '__main__':
	# Parse the arguments
	args = get_args()

	# Raw print arguments
	print("You are running the script with arguments: ")
	for a in args.__dict__:
		print(str(a) + ": " + str(args.__dict__[a]))

	csv.field_size_limit(1000000000)  # up the field size because stories are long

	id_csv = args.id_csv
	out_csv = args.out_csv
	first_id = str(args.first_id)
	last_id = str(args.last_id)

	if (None is first_id) and (None is last_id):
		raise ValueError("Either the first or last id have to be specified.")

	# clean extension
	if ".csv" not in id_csv:
		id_csv = id_csv + ".csv"

	with open(id_csv, 'r+', newline="") as f_in:
		reader = csv.reader(f_in)
		with open(out_csv + ".csv", 'a', newline="") as f_out:
			writer = csv.writer(f_out, delimiter=',')
			if None is first_id:
				should_copy = True
			else:
				should_copy = False
			for row in reader:
				if not row:
					continue
				should_copy = compare_id(row[0], first_id, last_id, should_copy)
				if should_copy is "last":
					print("The last id has been reached.")
					break
				elif should_copy is False:
					print('Skipping id to be excluded')
				else:
					writer.writerow(row)

	print("Done.")


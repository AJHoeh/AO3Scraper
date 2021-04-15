import csv
import argparse
import ntpath


def get_args():
	parser = argparse.ArgumentParser(description='Removes ids before/after certain id.')
	parser.add_argument(
		'id_csv',
		metavar='csv',
		help='The name of the csv with the ids.',
		type=str
	)

	parser.add_argument(
		'--out_csv', metavar='out_csv',
		help='The name of the csv to write the cut file to.',
		default=None,
		type=str
	)

	parser.add_argument(
		'--first_id', metavar='first_id',
		help='The first id you want to keep.',
		type=int,
		default=None
	)

	parser.add_argument(
		'--last_id', metavar='last_id',
		help='The last id you want to keep.',
		type=int,
		default=None
	)

	return parser.parse_args()


def compare_id(fic_id, first, last, should_copy):
	if int(fic_id) == first:
		return True
	elif int(fic_id) == last:
		return "last"
	else:
		return should_copy


def get_path_parts(path):
	head, tail = ntpath.split(path)
	if tail:
		file = tail
		directory = ntpath.dirname(path)
	else:
		file = ntpath.basename(head)
		directory = ntpath.dirname(head)

	basename, ext = ntpath.splitext(file)
	return directory, basename, ext


def create_file_name(original_name, extension, prefix=None, suffix=None):
	directory, basename = get_path_parts(original_name)[:2]

	if prefix:
		basename = prefix + basename
	if suffix:
		basename += suffix
	basename += extension

	return directory+"/"+basename


def main():
	# Parse the arguments
	args = get_args()
	ext = ".csv"

	# Raw print arguments
	print("You are running the script with arguments: ")
	for a in args.__dict__:
		print(str(a) + ": " + str(args.__dict__[a]))

	csv.field_size_limit(1000000000)  # up the field size because stories are long

	id_csv = args.id_csv
	out_csv = args.out_csv
	first_id = args.first_id
	last_id = args.last_id

	if (None is first_id) and (None is last_id):
		raise ValueError("Either the first or last id have to be specified.")

	if None is out_csv:
		out_csv = create_file_name(id_csv, ext, suffix="_cut")
	else:
		out_csv = create_file_name(out_csv, ext)

	print("Writing to "+out_csv)

	with open(id_csv, 'r+', newline="") as f_in:
		reader = csv.reader(f_in)
		with open(out_csv, 'a', newline="") as f_out:
			writer = csv.writer(f_out, delimiter=',')
			if None is first_id:
				should_copy = True
			else:
				should_copy = False
			for row in reader:
				if not row:
					continue
				should_copy = compare_id(row[0], first_id, last_id, should_copy)
				if should_copy == "last":
					print("The last id has been reached.")
					break
				elif not should_copy:
					print('Skipping id to be excluded')
				else:
					writer.writerow(row)

	print("Done.")


main()

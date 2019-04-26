
import csv


def load_csv(path, delimiter=',', remove_duplicates=False):
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)

        # Ignore header
        next(reader)

        if remove_duplicates:
            return {tuple(row) for row in reader}
        else:
            return [row for row in reader]


def dump_csv(fieldnames, data, output_file, delimiter=','):
    with open(output_file, 'w') as f:
        writer = csv.writer(f, dialect='unix', fieldnames=fieldnames,
                            delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)


import os
import random

from . import ioutils


random_gen = random.SystemRandom()


def compare(ref, files, output,
            percentage=True, count=False, delimiter=','):
    comparsion = []
    ref_data = ioutils.load_csv(ref, delimiter=delimiter,
                                remove_duplicates=True)
    for path in files:
        data = ioutils.load_csv(path, delimiter=delimiter,
                                remove_duplicates=True)

        common = ref_data & data

        res = []
        count = len(common)

        if percentage:
            res.append(str(count/len(data)).replace('.', ','))
        if count:
            res.append(count)

        comparsion.append(res)

    fieldnames = []

    if percentage:
        fieldnames.append('percentage')
    if count:
        fieldnames.append('count')

    ioutils.dump_csv(fieldnames, comparsion, output)


def split(headers, csv_data, output,
          split_size=1, shuffle=False, delimiter=','):
    if shuffle:
        random_gen.shuffle(csv_data)

    if delimiter is None:
        delimiter = '\0'
    elif type(delimiter) is not str:
        raise TypeError('The delimiter must be a string')

    row_count = len(csv_data)
    split_number = row_count//split_size

    if row_count % split_size > 0:
        split_number += 1

    for i in range(split_number):
        if i < row_count:
            sp = csv_data[i*split_size:(i+1)*split_size]
        else:
            sp = csv_data[i*split_size:]

        ioutils.dump_csv(headers, sp,
                         os.path.join(output, str(i+1)),
                         delimiter)


def extract(headers, csv_data, output,
            size, shuffle=False, delimiter=','):
    if shuffle:
        random_gen.shuffle(csv_data)

    if delimiter is None:
        delimiter = '\0'
    elif type(delimiter) is not str:
        raise TypeError('The delimiter must be a string')

    row_count = len(csv_data)

    if size < 1 or size > row_count:
        raise ValueError('Invalid size to extract')

    selected_rows = random.sample(csv_data, size)

    ioutils.dump_csv(headers, selected_rows, output, delimiter)

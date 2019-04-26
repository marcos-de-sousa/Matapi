
import argparse
import csv
import os
import sys

from .operations import compare, extract, split


parser = argparse.ArgumentParser(
        prog='csv-split',
        description='Split, extract and compare csv files.')

parser.add_argument('file', help='input csv file')

op_group = parser.add_mutually_exclusive_group(required=True)
op_group.add_argument('-s', '--split-size',
                      help='size of splits',
                      type=int, metavar='',
                      dest='split_size')
op_group.add_argument('-n', '--split-number',
                      help='number of splits',
                      type=int, metavar='',
                      dest='split_number')
op_group.add_argument('-e', '--extract',
                      help='extract N lines from csv',
                      type=int, metavar='')
parser.add_argument('-c', '--compare', help='compare files to input',
                    nargs='+', metavar='FILE')
parser.add_argument('-r', '--repeat', help='repeat this command N times',
                    type=int, metavar='', default=1)
parser.add_argument('-o', '--output', help='output directory',
                    type=str, metavar='')
parser.add_argument('--delimiter', help='separator used on csv file',
                    type=str, metavar='', default=',')
parser.add_argument('--shuffle', help='shuffle the csv before spliting',
                    action='store_true')
parser.add_argument('--unique', help='remove duplicates from csv',
                    action='store_true')


def _split_csv_data(csv_data, output,
                    split_size, shuffle, delimiter):
    split(list(csv_data), output, split_size=split_size,
          shuffle=shuffle, delimiter=delimiter)


def extract_csv(headers, csv_data, args):
    for i in range(args.repeat):
        extract_path = os.path.join(args.output, str(i+1))

        print(f'List {i+1}... ', end='')

        try:
            extract(headers, list(csv_data), extract_path, size=args.extract,
                    shuffle=args.shuffle, delimiter=args.delimiter)
        except Exception as e:
            print('FAIL')
            print(e, file=sys.stderr)
            sys.exit(1)

        print('OK')


def split_csv(headers, csv_data, args):
    split_size = 1

    if args.split_size is not None:
        split_size = args.split_size

    if args.split_number is not None:
        split_size = len(csv_data)//args.split_number

    remainder = len(csv_data) % split_size
    if remainder != 0:
        print(f'WARNING: Last split will have {remainder} rows',
              file=sys.stderr)

    if args.repeat == 1:
        try:
            _split_csv_data(headers, csv_data, args.output, split_size,
                            args.shuffle, args.delimiter)
        except Exception as e:
            print('Failed to split csv')
            print(e, file=sys.stderr)
            sys.exit(1)

        return

    for i in range(args.repeat):
        split_dir = os.path.join(args.output, str(i+1))

        print(f'Split {i+1}... ', end='')

        try:
            os.mkdir(split_dir)
        except OSError as e:
            print('FAIL')
            print(e, file=sys.stder)
        try:
            _split_csv_data(headers, csv_data, split_dir, split_size,
                            args.shuffle, args.delimiter)
        except OSError as e:
            print('FAIL')
            print(e, file=sys.stder)
            sys.exit(1)

        print('OK')


def run():
    args = parser.parse_args()

    csv_file = None

    if args.output is None:
        args.output = os.getcwd()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if not args.file or args.file == '-':
        csv_file = sys.stdin
    else:
        try:
            csv_file = open(args.file)
        except OSError:
            print(f'Failed to open file: {args.file}', file=sys.stderr)
            sys.exit(1)

    with csv_file:
        try:
            reader = csv.reader(csv_file, delimiter=args.delimiter)
        except csv.Error as e:
            print('Failed to read csv file', file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)

        headers = next(reader)

        if args.unique:
            csv_data = set(tuple(row) for row in reader)
        else:
            csv_data = list(reader)

        if args.extract is not None:
            method = extract_csv
        else:
            method = split_csv

        method(headers, csv_data, args)

        if args.compare:
            compare(csv_data, args.compare, delimiter=args.delimiter)

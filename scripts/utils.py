import datetime, json, os, errno
import sys
import subprocess as sp
import gzip
import pickle as pkl


def flush_output(stuff, print_time=False):
    if not print_time:
        print(stuff)
    else:
        print(f"{datetime.datetime.now()}: {stuff}")
    sys.stdout.flush()


def mkdirs(newdir, mode=0o755):
    try: os.makedirs(newdir, mode)
    except OSError as err:
        # Reraise the error unless it's about an already existing directory
        if err.errno != errno.EEXIST or not os.path.isdir(newdir):
            raise

def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def silent_copy(infile, outfile):
    os.system(f'cp {infile} {outfile}')


def copy_file_to_directory(file_path, dir_path):
    if not os.path.isdir(dir_path):
        print("Given directory path is not a directory..")
        cmd = 'mkdir -p {}'.format(dir_path)
        os.system(cmd)
        print("Created directory for - '{}'".format(dir_path))

    cmd = 'cp {} {}'.format(file_path, dir_path)
    os.system(cmd)
    return


def read_lines(file_name):
    if not file_name.endswith(".gz"):
        with open(file_name, 'r') as f:
            lines = [l.strip() for l in f.readlines() if len(l.strip())]
    else:
        with gzip.open(file_name, 'rt') as f:
            lines = [l.strip() for l in f.readlines() if len(l.strip())]

    return lines


def write_lines(lines, file_name, mode='w'):
    if not os.path.isfile(file_name):
        cmd = "touch {}".format(file_name)
        _ = os.system(cmd)

    if mode == 'w':
        with open(file_name, 'w') as f:
            f.write('\n'.join([str(line) for line in lines])+'\n')
    elif mode == 'a':
        curr_lines = ReadLines(file_name)
        WriteLines(curr_lines + lines, file_name)
    else:
        print("Given mode '{}' not supported".format(mode))

    return


def get_io_wrapper(file_name, mode=None):
    """Get Wrapper to read a file name line by line. Useful to pass to functions which need all lines from a file

    Args:
        file_name (str): Path to file
        mode (str): Mode (usually 'r' or 'rt' or 'rb')

    Returns:
        _io.TextIOWrapper 
    """
    if file_name.strip().endswith('.gz'):
        if mode is None:
            mode = 'rt'

        return gzip.open(file_name, mode)
    else:
        if mode is None:
            mode = 'r'

        return open(file_name, mode)


def get_command_output(cmd):
    """
    Get output of bash command
    """
    return sp.check_output(cmd, shell=True).decode('utf-8').strip()


def replace_user_in_file_path(file_name, user):
    """Replace user name in give file path

    Args:
        file_name (str): Path to file
        user (str): New user to replace with

    Returns:
        str: New file path
    """
    file_items = [x.strip()
                  for x in file_name.strip().split('/') if len(x.strip())]
    file_items[1] = user

    return "/" + '/'.join(file_items).strip()


def flatten(list_of_lists):
    """Flatten a given list of lists

    Args:
        list_of_lists (list): Given list of lists

    Returns:
        list: Flattened list
    """
    return [x for each_list in list_of_lists for x in each_list]


def create_directory(dir_name):
    """Create directory
    """
    try:
        # _ = os.mkdir(dir_name)
        cmd = f"mkdir -p {dir_name}"
        _ = os.system(cmd)
        return
    except Exception:
        return 
        
def copy_file_to_dir(file_name, dir_name):
    """Copy file to given directory and return new file name

    Args:
        file_name (str): Path to file
        dir_name (str): Path to directory

    Returns:
        str: New file path
    """
    create_directory(dir_name)
    
    cmd = "cp {} {}".format(file_name, dir_name)
    os.system(cmd)
    
    return os.path.join(dir_name, os.path.basename(file_name))


def copy_files_to_dir(files, dir_name):
    """Copy multiple files to directory
    """
    return [copy_file_to_dir(file_name, dir_name) for file_name in files]


def remove_lines_from_file(file_name, substring):
    """Remove all lines from give file which contain given substring

    Args:
        file_name (str): Path to file
        substring (str): Substring to search in file
    """
    lines = [x for x in ReadLines(file_name) if substring not in x]
    WriteLines(lines, file_name)
    return


def add_lines_to_file(file_name, new_lines):
    """Add given line to end of file

    Args:
        file_name (str): Path to file
        new_lines (list): List of strings to add at the end of file
    """
    WriteLines(new_lines, file_name, mode='a')
    return

def remove_duplicates(any_list):
    """Remove duplicates without changing order of items

    Args:
        any_list (list): List of items

    Returns:
        list: List without duplicates
    """

    final_list = list()
    for item in any_list:
        if item not in final_list:
            final_list.append(item)

    return final_list


def load_map_from_file(file_name):
    """Load data into map from given file.

    Expects file to be in the format
    '
    ...
    ABC 45.0
    DEF 32.1
    ...
    '

    Args:
        file_name (str): Path to file

    Returns:
        dict: Mapping loaded from file
    """
    lines = ReadLines(file_name)

    file_map = dict()
    for line in lines:
        tokens = [x.strip() for x in line.strip().split(' ') if len(x.strip())]
        file_map[tokens[0]] = float(tokens[1])

    return file_map

def store_data(data, file_path):
    """
    Store data in pickle file
    Args:
        data: data to be stored
        file_path: file name
    """
    f = open(file_path, 'wb')
    pkl.dump(data, f)
    f.close()
    return
    
def load_data(file_path):
    """
    Load data from given file
    Args:
        file_path: file name
    """
    f = open(file_path, 'rb')
    data = pkl.load(f)
    f.close()
    return data

def join_files(file1, file2, col1, col2, out_cols1, out_cols2, output_file = None):
    """
    Join(inner) two files based on a common column
    Args:
        file1, file2: input files
        col1, col2: index of common column in file1, file2
        out_cols1, out_cols2: index of columns from file1, file2 required in output

        eg: join_files(file1, file2, 1, 1, [2, 3], [2, 3, 4])
    """
    output_cols = ','.join([f"1.{i}" for i in out_cols1] + [f"2.{i}" for i in out_cols2])
    join_cmd = f"join -1 {col1} -2 {col2} -e0 -o'0,{output_cols}' {file1} {file2} "
    if output_file is not None:
        os.system(join_cmd + f"> {output_file}")
    return join_cmd


def join_files_alt(file1, file2, col1, col2, out_cols_str, output_file=None):
    """"""
    join_cmd = f"join -1 {col1} -2 {col2} -e0 -o'0,{out_cols_str}' {file1} {file2} "
    if output_file is not None:
        _ = os.system(join_cmd + f"> {output_file}")
    return join_cmd


def count_cols_in_file(file_name, sep):
    # cmd = f"head -n1 {file_name} | tr '{sep}' '\n' | wc -l"
    # return int(get_command_output(cmd))
    fl = get_command_output(f"head -n1 {file_name}")
    return len([x.strip() for x in fl.strip().split(sep)])


def join_two_files_util(file1, file2, outfile, numDummy1=0, numDummy2=0, exact_or_asof_flag=1, 
                    executable=os.path.join(os.getenv("HOME"), 'bin', 'join')):
    """Use cpp utility to join files based on first column
    """
    if not os.path.isfile(executable):
        raise Exception(f"Executable not found for join: {executable}")

    cmd = f"{executable} {exact_or_asof_flag} {file1} {file2} {outfile} {numDummy1} {numDummy2}"
    _ = os.system(cmd)
    
    return

    
def join_mult_files_util(files, outfile, numDummys=None, exact_or_asof_flag=1,
                    executable=os.path.join(os.getenv("HOME"), 'bin', 'join')):
    """Use cpp utility to join more two or more files based on first column in each file
    """
    if not os.path.isfile(executable):
        raise Exception(f"Executable not found for join: {executable}")

    if len(files) < 2:
        raise Exception(f"Provide atleast two files to join..")

    if numDummys is None:
        numDummys = [0 for _ in files]
    
    if len(files) != len(numDummys):
        raise Exception(f"Number of files not equal to number of dummy params")

    if len(files) == 2:
        join_two_files_util(files[0], files[1], outfile, numDummys[0], numDummys[1], exact_or_asof_flag, executable)
        return

    tmp_zero = outfile + ".tmp0"
    tmp_one = outfile + ".tmp1"

    join_two_files_util(files[0], files[1], tmp_zero, numDummys[0], numDummys[1], exact_or_asof_flag, executable)
    curr_idx = 0
    
    for file_name, numDummy in zip(files[2:], numDummys[2:]):
        curr_in_file = tmp_zero if curr_idx == 0 else tmp_one
        curr_out_file = tmp_one if curr_idx == 0 else tmp_zero
        
        join_two_files_util(curr_in_file, file_name, curr_out_file, 0, numDummy, exact_or_asof_flag, executable)
        
        curr_idx = 1 - curr_idx
    
    final_tmp_file = tmp_zero if curr_idx == 0 else tmp_one
    rem_tmp_file = tmp_one if curr_idx == 0 else tmp_zero
    
    _ = os.system(f"touch {outfile}")
    _ = os.system(f"mv {final_tmp_file} {outfile}")
    _ = os.system(f"rm {rem_tmp_file}")
    
    return
    
    
def divide_into_chunks(array, chunk_size):
    """Divide a given iterable into pieces of a given size
    
    Args:
        array (list or str or tuple): Subscriptable datatypes (containers)
        chunk_size (int): Size of each piece (except possibly the last one)
        
    Returns:
        list or str or tuple: List of chunks
    """
    return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)] 

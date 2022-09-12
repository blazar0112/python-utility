import os
import argparse
import shutil
from chardet import detect

# get file encoding type
def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def cleanse(source_directory, output_directory):
    shutil.rmtree(output_directory)
    os.mkdir(output_directory)
    for dirpath, _, filenames in os.walk(source_directory, topdown=True):
        filenames.sort()
        for filename in filenames:
            source_filepath = os.path.abspath(os.path.join(dirpath, filename))
            from_codec = get_encoding_type(source_filepath)
            print('source file [', source_filepath, '] encoding [', from_codec, ']', sep='')
            if from_codec!='UTF-8' and from_codec!='UTF-8-SIG' and from_codec!='ascii':
                # may detect wrongly like GB2312
                source_codec = 'Big5'
            else:
                source_codec = from_codec

            output_filepath = os.path.abspath(os.path.join(output_directory, filename))

            try:
                print('Writing to file [', output_filepath, ']', sep='')
                with open(source_filepath, 'r', encoding=source_codec) as source_file, \
                    open(output_filepath, 'w', encoding='utf-8', newline='\n') as output_file:
                    text = source_file.read()
                    output_file.write(text)
            except UnicodeDecodeError:
                print('Decode Error')
            except UnicodeEncodeError:
                print('Encode Error')

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description=f'Cleanse all files in a directory.')
    #parser.add_argument('sourceDirectory', help=f'source directory.')
    #parser.add_argument('outputDirectory', help=f'output directory.')
    #args = parser.parse_args()

    cleanse('source', 'output')

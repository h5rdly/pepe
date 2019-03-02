import tempfile, readline #, cmd
from subprocess import Popen, PIPE
from configparser import ConfigParser  #, ExtendedInterpolation, BasicInterpolation
from collections import Counter


def get_config(conf_file = 'pepe.ini'):
    '''  '''
    
    default_config = '''
    [Toolchain]
      compiler = clang
    [Paths]
      compiler = clang
    ''' 
    
    config = ConfigParser()
    try:
        config.read_file(open('conf_file'))
    except Exception as e:
        print ('Exception reading config file: ', e)
        config.read_string(default_config)
        with open('pepe.ini', 'w') as conf:
            config.write(conf)


    return config


def interpret(code, compiler = 'clang'):
    ''' '''

    interpret = Popen((compiler, '-xc++', '-'), stdin = PIPE, stdout = PIPE, stderr = PIPE)
    res, err = interpret.communicate(code.encode('utf-8'))


    return res, err


def mainloop(prompt = 'pepe> ', config = None):
    '''  '''
    
    # Setup config and file for managing the incoming code
    config = config or get_config()
    pepe_file = tempfile.SpooledTemporaryFile(mode='a+t')
    pepe_file.write('\n'.join(('#include <stdio.h>', 'int main()', '{', '}')))
    compiler = config['Paths']['compiler']
    tab = ' ' * 4
    block_depth = 1  

    while True:
        line = input(prompt + tab*(block_depth - 1))
        # Remove finishing '}' and add new line
        pepe_file.seek(pepe_file.tell() - 1)  # 1 back from current position
        pepe_file.truncate()
        pepe_file.write(tab * block_depth + line + ';\n')   # No need to add ;

        counter = Counter(line)
        block_depth += line.count('{') - line.count('}')
        if not block_depth > 1:
            # Close up and interpret pepe
            pepe_file.write('}')
            pepe_file.seek(0)
            code = pepe_file.read()
            print ("code:\n", code)
            res, err = interpret(code, compiler)
            print ("result:\n", res)
            print ("error:\n", err)


if __name__=='__main__':

    from sys import argv as args

    # Managing being used on an actual (hot) code file

    mainloop()

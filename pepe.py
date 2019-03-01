import tempfile #, cmd
from subprocess import Popen, PIPE
from configparser import ConfigParser  #, ExtendedInterpolation, BasicInterpolation


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
        config.read(conf_file)
    except Exception as e:
        print ('Exception reading config file: ', e)
        config.read_string(default_config)
        with open('pepe.ini', 'w') as conf:
            config.write(conf)


    return config


def interpret(code, compiler = 'clang'):
    ''' '''

    interpret = Popen(('clang'), stdin = PIPE, stdout = PIPE, stderr = PIPE)
    res, err = interpret.communicate(code.encode('utf-8'))


    return res, err


def mainloop(prompt = 'pepe> ', config = None):
    '''  '''
    
    # Setup config and file for managing the incoming code
    config = config or get_config()
    pepe_file = tempfile.SpooledTemporaryFile(mode='a+t')
    pepe_file.write('\n'.join(('#include <stdio.h>', 'int main()', '{', '')))
    
    compiler = config['Paths']['compiler']
    tab = ' ' * 4
    tabdepth = 1   # Counts how many tabs to add to keep the pepe code formatted for viewing
    

    while True:
        line = input(prompt)
        if not line.endswith('{'):
            # Don't have to add ;
            pepe_file.write(tab * tabdepth + line + ';\n}')
    
            # Interpret pepe
            pepe_file.seek(0)
            code = pepe_file.read()
            print ("code:\n", code)
            res, err = interpret(code, compiler)
            print ("result:\n", res)


if __name__=='__main__':

    from sys import argv as args

    # Managing being used on an actual (hot) code file

    mainloop()

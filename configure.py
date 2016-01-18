import os, sys
import argparse
from configobj import ConfigObj, flatten_errors
from validate import Validator, ValidateError

def check_file_exist(path, exception_type):
    if not os.path.isfile(path):
        raise exception_type('{0} does not exist'.format(path))
    if not os.access(path, os.R_OK):
        raise exception_type('{0} is not accessible'.format(path))
    return path

def check_file_exist_argparse(path):
    return check_file_exist(path, argparse.ArgumentTypeError)

def check_file_exist_config(path):
    return check_file_exist(path, ValidateError)

def read_config(config_path='config.ini', configspec_path='configspec.ini'):
    config = ConfigObj(check_file_exist_config(config_path), configspec=check_file_exist_config(configspec_path))
    validator = Validator({'filepath': check_file_exist_config})
    results = config.validate(validator, preserve_errors=True)

    if results != True:
        for (section_list, option, error) in flatten_errors(config, results):
            section = ', '.join(section_list)
            if option is not None:
                if error:
                    print('The "{0}" key in the section "{1}" failed validation with error: {2}.'.format(option, section, error))
                else:
                    print('Option "{0}" in section "{1}" was missing.'.format(option, section))
            else:
                print('The following section was missing: {0}'.format(section))
        print('Config file validation failed!')
        sys.exit(1)
    else:
        return config


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Configuration loader.', prog='Citizen Sensor')
    parser.add_argument('-c', '--config', help='Path to ini config file', default='config.ini', type=check_file_exist_argparse)
    parser.add_argument('-s', '--spec', help='Path to ini config spec file', default='configspec.ini', type=check_file_exist_argparse)
    args = parser.parse_args()
    config = read_config()


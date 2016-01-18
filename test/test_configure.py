import os
import configure
from unittest import TestCase
from configobj import ConfigObj
from validate import ValidateError
from nose.tools import assert_equals, assert_raises

class TestConfigure(TestCase):

    def setUp(self):
        config = ConfigObj()
        config.filename = 'test/config-test.ini'
        config['user'] = 'pinkiepie'
        config['password'] = 42
        config['path'] = 'image_classifier.py'
        config.write()

        config.filename = 'test/config-test-fail.ini'
        config['password'] = 42.5
        config.write()

        configspec = ConfigObj()
        configspec.filename = 'test/configspec-test.ini'
        configspec['user'] = 'string'
        configspec['password'] = 'integer'
        configspec['path'] = 'filepath'
        configspec.write()
        self.files_for_cleanup = ['test/config-test.ini', 'test/config-test-fail.ini', 'test/configspec-test.ini']

    def test_check_file_exists_throws_exception_on_missing_file(self):
        with assert_raises(ValidateError) as cm:
            configure.check_file_exist_config('dummy')

    def test_check_file_exists(self):
        filename = 'test-file.tmp'
        f = open(filename, 'w')
        assert_equals(filename, configure.check_file_exist_config(filename))
        os.remove(filename)

    def test_config_read_success(self):
        config = configure.read_config('test/config-test.ini', 'test/configspec-test.ini')
        assert_equals(config['user'], 'pinkiepie')
        assert_equals(config['password'], 42)
        assert(os.path.isfile(config['path']))

    def test_config_read_validate_fail(self):
        assert_raises(SystemExit, configure.read_config, 'test/config-test-fail.ini', 'test/configspec-test.ini')

    def test_config_missing(self):
        assert_raises(ValidateError, configure.read_config, 'config-missing.ini', 'configspec.ini')

    def test_configspec_missing(self):
        assert_raises(ValidateError, configure.read_config, 'config-missing.ini', 'configspec.ini')

    def tearDown(self):
        [os.remove(path) for path in self.files_for_cleanup]
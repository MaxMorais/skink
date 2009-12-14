#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright Bernardo Heynemann <heynemann@gmail.com>

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fudge import Fake, with_fakes, with_patched_object
from fudge.inspector import arg
from fudge_extensions import clear

import skink.lib.ion.settings as sets
from skink.lib.ion import Settings

parser = (Fake("ConfigParser").expects("__init__")
                              .expects("read")
                              .with_args(arg.endswith("config.ini")))

@with_fakes
@with_patched_object(sets, "ConfigParser", parser)
def test_can_create_settings():
    settings = Settings("some_dir")

    assert settings

@with_fakes
@with_patched_object(sets, "ConfigParser", parser)
def test_settings_will_load_config_ini():
    settings = Settings("some_dir")

    settings.load()

@with_fakes
@with_patched_object(sets, "ConfigParser", parser)
def test_settings_will_load_config_ini_retains_config():
    settings = Settings("some_dir")

    settings.load()

    assert settings.config

custom_file_parser = (Fake("ConfigParser").expects("__init__")
                                          .expects("read")
                                          .with_args(arg.endswith("custom.ini")))

@with_fakes
@with_patched_object(sets, "ConfigParser", custom_file_parser)
def test_settings_can_load_custom_file():
    settings = Settings("some_dir")

    settings.load("custom.ini")

    assert settings.config

@with_fakes
@with_patched_object(sets, "ConfigParser", custom_file_parser)
def test_read_attribute_before_load_gives_error():
    settings = Settings("some_dir")

    try:
        assert settings.SomeSection.SomeAttribute
    except RuntimeError, err:
        assert str(err) == "You can't use any settings before loading a config file. Please use the load method."
        return

    assert False, "Should not have gotten this far"

get_attr_parser = (Fake("ConfigParser").expects("__init__")
                                          .expects("read")
                                          .with_args(arg.endswith("config.ini"))
                                          .expects("get")
                                          .with_args("SomeSection", "SomeAttribute")
                                          .returns("attribute_value"))

@with_fakes
@with_patched_object(sets, "ConfigParser", get_attr_parser)
def test_settings_read_attribute_returns_config_read():
    settings = Settings("some_dir")
    settings.load()

    assert settings.SomeSection.SomeAttribute == "attribute_value"

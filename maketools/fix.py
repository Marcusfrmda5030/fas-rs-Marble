#!/bin/python3
# Copyright 2023 shadow3aaa@gitbub.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from maketools.toolchains import Buildtools
from pathlib import Path


def __clippy_fix(tools: Buildtools, arg: str = ""):
    (
        tools.cargo()
        .arg("clippy --fix --allow-dirty --allow-staged --target aarch64-linux-android")
        .arg(arg)
        .build()
    )

    (
        tools.cargo()
        .arg(
            "clippy --fix --allow-dirty --allow-staged --target aarch64-linux-android --release"
        )
        .arg(arg)
        .build()
    )


def task():
    tools = Buildtools()

    os.system("ruff check --fix make.py")
    os.system("ruff check --fix maketools")

    __clippy_fix(tools)
    __clippy_fix(tools, "--features use_binder --no-default-features")

    os.chdir("zygisk")
    (
        tools.cpp_tidy()
        .arg("-fix-errors")
        .arg("--fix")
        .arg("--header-filter='.*.cpp'")
        .arg(
            "{} -- -I{}".format(
                Path("src").joinpath("*.cpp"), Path("rust").joinpath("include")
            )
        )
        .tidy()
    )

    os.chdir("rust")
    __clippy_fix(tools)

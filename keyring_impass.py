#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Very simple wrapper around impass to use it with keyring"""

__version__ = "0.1.0"

import json
import os
import subprocess
from contextlib import contextmanager

import keyring.backend


@contextmanager
def updated_env(**kwargs):
    """Temporarily update the environment. To be used in a with statement"""
    oldenv = dict(os.environ)
    for k, v in kwargs.items():
        if v is None and k in os.environ:
            del os.environ[k]
        else:
            os.environ[k] = v
    yield
    os.environ.clear()
    os.environ.update(oldenv)


class ImpassKeyring(keyring.backend.KeyringBackend):
    priority = 6

    def set_password(self, _, username, password):
        raise NotImplementedError

    def get_password(self, _, username):
        key = username
        try:
            with updated_env(IMPASS_DUMP_PASSWORDS="1"):
                return json.loads(
                    subprocess.check_output(
                        [
                            "impass",
                            "dump",
                            key,
                        ]
                    )
                    .decode("utf-8")
                    .strip()
                )[key]["password"]
        except KeyError:
            return None

    def delete_password(self, servicename, username, password):
        raise NotImplementedError

# -*- coding: utf-8 -*-

from soft_deps import api


def test():
    _ = api


if __name__ == "__main__":
    from soft_deps.tests import run_cov_test

    run_cov_test(
        __file__,
        "soft_deps.api",
        preview=False,
    )

# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from soft_deps.tests import run_cov_test

    run_cov_test(
        __file__,
        "soft_deps",
        is_folder=True,
        preview=False,
    )

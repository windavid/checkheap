import os
import copy
from subprocess import Popen, PIPE
import pathlib


def launch(ph_elf):
    # TODO: library version check

    # in case of crash no libc output traces will be printed on this script side
    env = copy.copy(os.environ)
    env["LIBC_FATAL_STDERR_"] = "1"

    proc = Popen(str(ph_elf.absolute()), stdout=PIPE, stderr=PIPE, env=env)
    out, err = proc.communicate()
    if proc.returncode != 0:
        return True, None
    serr = err.decode('ascii')
    errlines = serr.splitlines()
    return False, errlines


def iterate_checks(checks_dir):
    checks_dir = pathlib.Path(checks_dir)
    for src in checks_dir.glob('c_*.c'):
        check_file = checks_dir / src.stem
        assert check_file.exists(), "Check file {} was not compiled, launch make all first".format(str(check_file))
        check_name = check_file.name[2:].replace('_', ' ')
        yield check_file, check_name


def check_case(ph_elf, check_name):
    pref = "{:.<30}".format(check_name)
    err, errlines = launch(ph_elf)
    if err or not errlines:
        print(pref, "ERROR")
        return
    diffline = errlines[-1]
    """
    TODO:
    GOTDIFF replace with several possible keys:
    ALLOCATED_DIFF - for read|write allocated on controlled address
    """
    if diffline.startswith('GOTDIFF: '):
        diff = int(diffline[9:])
        result = ("OK", "WRONG")[diff]
        print(pref, result)
        return
    print(pref, "Incorrect check")


def check_all():
    for ph_elf, check_name in iterate_checks('./checkers'):
        check_case(ph_elf, check_name)


if __name__ == "__main__":
    check_all()

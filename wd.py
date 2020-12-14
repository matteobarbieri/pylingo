import subprocess

from colors import bcolors

from tempfile import NamedTemporaryFile


def paint_red(s):
    return f"{bcolors.FAIL}{s}{bcolors.ENDC}"


def paint_green(s):
    return f"{bcolors.OKGREEN}{s}{bcolors.ENDC}"


def check_next_line(proc, cur_line):

    # Read next line
    next_line = proc.stdout.readline()
    next_line_str = bytes.decode(next_line)
    next_line_str = next_line_str.rstrip("\n")

    inp_add = ""
    out_add = ""

    if not next_line or next_line_str[0] == ' ':

        if cur_line[0] == '+':
            inp_add += paint_green(cur_line[1:])
            out_add += "-"*len(cur_line[1:])

        if cur_line[0] == '-':
            out_add += paint_red(cur_line[1:])
            inp_add += "-"*len(cur_line[1:])

        if next_line:
            inp_add += next_line_str[1:]
            out_add += next_line_str[1:]

    elif next_line_str[0] == '+':

        if cur_line[0] == '-':

            str_diff = len(cur_line[1:]) - len(next_line_str[1:])
            if str_diff > 0:
                out_add += paint_red(cur_line[1:])
                inp_add += paint_green(next_line_str[1:] +
                                       '-'*str_diff)
            else:
                out_add += paint_red(cur_line[1:] + '-'*(-str_diff))
                inp_add += paint_green(next_line_str[1:])

    return inp_add, out_add


def check_solution(input_text: str, solution: str) -> None:

    with NamedTemporaryFile("w+") as f_inp, NamedTemporaryFile("w+") as f_sol:

        f_inp.write(input_text)
        f_inp.flush()

        f_sol.write(solution)
        f_sol.flush()

        check_solution_files(f_inp.name, f_sol.name)


def check_solution_files(input_file, sol_file):

    cmd_string = (
        "git diff --no-index --word-diff=porcelain --word-diff-regex=. "
        f"{input_file} {sol_file}"
        " | tail -n +6 | head -n -1")  # Cut the first 6 and last 1 lines

    # print(cmd_string)

    proc = subprocess.Popen(
        cmd_string, stdout=subprocess.PIPE, shell=True)

    inp_form = ""
    out_form = ""

    while True:
        line = proc.stdout.readline()
        if not line:
            break

        # the real code does filtering here
        # print ("test:", line.rstrip())
        # print(type(line))

        line_str = bytes.decode(line)
        line_str = line_str.rstrip("\n")

        # print(line_str)

        if line_str[0] in ['+', '-']:

            # inp_add, out_add = check_next_line(proc, line_str, inp_form, out_form)
            inp_add, out_add = check_next_line(proc, line_str)
            inp_form += inp_add
            out_form += out_add

        else:
            inp_form += line_str[1:]
            out_form += line_str[1:]

    print(f"Input:   {out_form}")
    print(f"Correct: {inp_form}")


if __name__ == "__main__":
    check_solution("AAA", "AABA")
    # main()

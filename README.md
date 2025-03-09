# uwaterloo-learn-checker
An easy-to-use tool for UWaterloo instructors/TAs to check the students' code downloaded from the LEARN platform, suporting file renaming, running in batch, and printing statistics. 

## Features

1. Single & batch execution – Runs tests on one or multiple submissions, with direct terminal output for single files.
2. Automated logging – Saves results in `passed.txt`, `failed.txt`, and errors in `errorlog.txt` to your given directory.
3. Progress & stats – Displays a progress bar and final pass/fail/error counts.

Know problem(s)

1. If the student code got runtime error or timeout, the log in the bulk running does not show the entire output. Please run the single file testing to show all outputs.

## How to run this code

Files that you have to modify:

1. Modify `src/run_test.py` – the function to call your checking code.
2. Replace `src/dummy_checker.py` - with your main checking code.


Steps:

1. Download all students' submissions and put the folder under this directory.

    The downloaded student submissions are named as `<a-mysterious-number>-<a-mysterious-number>-<last-name>-<first-name>.py` which is annoying. This tool can rename the files to `<last-name>-<first-name>.py` for you.

2. Replace the code in file `run_test.py` with your checking code. You may find the example `dummy_checker.py` as an example.

    Remember to follow the input output format and do not change the function / file names, or it won't be able to be imported by the main function.

    ```
    Input:
        module      : ModuleType, the module that contains the student's code file, where a function can be extracted.
        verbose     : bool, True if you want to print the failed test cases, False otherwise.

    Output: 
        flag        : bool, True if the test passed, False otherwise.

    Decorator input: 
        timeout     : int, the maximum time the test can run in seconds. 
    ```

3. Run all students' submissions:

    ```bash
    python3 main.py -d <student-folder> -o <log-file-name> -m <optional-roster-last-passed> --rename
    ```

    e.g.,

    ```bash
    python3 main.py -d <student-folder> -o logs --rename
    python3 main.py -d <student-folder> -o logs2 -m logs/passed.txt --verbose
    ```

    Renaming is recommended at the first run.

    In the second run, the `-m` option is used to pass the last passed students' file, so that the tool can skip the passed students and only run the failed ones.

    You can use the `--verbose` option to control the output verbosity in your checker code. The default is False.

4. Or run one student's submission:

    ```bash
    python3 main.py -f <student-file-path>
    python3 main.py -f <student-file-path> --verbose
    ```

    e.g.,

    ```bash
    python main.py -f <student-folder>/<last-name>-<first-name>.py
    ```

## Question & Feeback

If you have questions or find problems running this code, issues/PRs are welcomed! 

Hope making your TA life easier!

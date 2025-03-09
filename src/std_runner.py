"""A class to manage the file names, running, and statistics of the student submissions."""
import importlib.util
import io
import os
import pathlib
import re
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout
from typing import Callable, Dict, List, ModuleType, Tuple


class StudentCodeRunner:
    def __init__(self, submission_dir: str, output_dir: str, run_test: Callable, verbose: bool = False, rename: bool = False) -> None:
        self.submission_dir = submission_dir
        self.output_dir = output_dir
        self.verbose = verbose
        self.rename = rename
        self.students_passed: List[str] = []
        self.students_failed: List[str] = []
        self.stats: Dict[str, int] = {"total": 0, "passed": 0, "failed": 0, "error": 0}
        self.run_test = run_test

    def run(self) -> None:
        """Run all submissions."""
        if self.rename:
            self.renamer(self.submission_dir)

        student_files = self.get_filenames()
        print(f"\nProcessing {self.stats['total']} submissions...")
        for i, student_file in enumerate(student_files):
            self.process_submission(student_file, i)

        print("\n\nWriting results to files...")
        self.write_output("passed.txt", self.students_passed)
        self.write_output("failed.txt", self.students_failed)
        self.print_statistics()

    def renamer(self, directory: str) -> None:
        """Rename files to student's name."""
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                match = re.match(r"\d+-\d+_-_(.*?)_-_\w+_-_\w+\.py", filename)
                if match:
                    new_filename = match.group(1) + ".py"
                    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

    def get_filenames(self, filename_passed: str = None, single_file: str = None) -> List[str]:
        """Get the list of student files."""
        if single_file:
            return [os.path.basename(single_file)] if single_file.endswith(".py") else []

        passed_students = []
        if filename_passed:
            with open(filename_passed, "r") as f:
                passed_students = [line.strip() for line in f.readlines()]
        
        files = [f for f in os.listdir(self.submission_dir) if f.endswith(".py") and f.removesuffix(".py") not in passed_students]
        self.stats["total"] = len(files)
        return files

    def load_module(self, student_file: str) -> Tuple[str, ModuleType]:
        """Load a single student's module."""
        student_name = student_file.replace(".py", "")
        student_path = os.path.join(self.submission_dir, student_file)
        spec = importlib.util.spec_from_file_location(student_name, student_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return student_name, module

    def run_single_test(self, module: ModuleType, single_file: bool = False) -> Tuple[bool, str]:
        """Run a single test."""
        if single_file:
            result = self.run_test(module, verbose=self.verbose)
            return result, ""
        else:
            stdout_buffer, stderr_buffer = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                result = self.run_test(module, verbose=self.verbose)
            output_log = "STDOUT:\n" + stdout_buffer.getvalue()
            if stderr_buffer.getvalue():
                output_log += "\nSTDERR:\n" + stderr_buffer.getvalue()
            return result, output_log

    def process_submission(self, student_file: str, current: int, single_file: bool = False) -> None:
        """Update the statistics of a single submission."""
        student_name, module = self.load_module(student_file)
        try:
            passed, output_log = self.run_single_test(module, single_file)
            if passed:
                self.students_passed.append(student_name)
                self.stats["passed"] += 1
                print(f"{student_file} PASSED") if single_file else None
            else:
                self.students_failed.append(student_name)
                self.stats["failed"] += 1
                if single_file:
                    print(f"{student_file} FAILED:\n{output_log}")
                else:
                    self.write_to_log(f"{student_name}: Test failed\n{output_log}\n{'='*50}")
        except Exception as e:
            self.students_failed.append(student_name)
            self.stats["error"] += 1
            error_msg = f"{student_name}: Runtime error - {str(e)}\nTraceback:\n{traceback.format_exc()}\n{'='*50}"
            print(error_msg) if single_file else self.write_to_log(error_msg)
        if not single_file:
            self.update_progress(current, student_name)

    def write_to_log(self, message: str) -> None:
        """Write the error log to a file."""
        errorlog_path = os.path.join(self.output_dir, "errorlog.txt")
        with open(errorlog_path, "a") as f:
            f.write(message + '\n')

    def write_output(self, filename: str, student_list: List[str]) -> None:
        """Write the list of students to a file."""
        pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(self.output_dir, filename), "w") as f:
            for student in student_list:
                f.write(student + "\n")

    def update_progress(self, current: int, student_name: str) -> None:
        """Print the progress to the terminal."""
        total, progress = self.stats["total"], (current + 1) * 100 // self.stats["total"]
        bar_length, filled_length = 40, int(40 * (current + 1) / total)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        sys.stdout.write(f'\r[{bar}] {progress}% | {current + 1}/{total} | {student_name}')
        sys.stdout.flush()

    def print_statistics(self) -> None:
        """Print the statistics to the terminal after running all."""
        print(f"\n{'=' * 50}\nTotal: {self.stats['total']} | Passed: {self.stats['passed']} | Failed: {self.stats['failed']} | Errors: {self.stats['error']}\n{'=' * 50}")

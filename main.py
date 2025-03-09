"""An assignment checking script for the LEARN platform downloaded student codes."""
import argparse
import os

from src.run_test import run_test
from src.std_runner import StudentCodeRunner


def main():
    """Main file to parse command line arguments and run the checker."""
    # parse arguments
    parser = argparse.ArgumentParser(description="Check student answers.")
    parser.add_argument("-d", type=str, help="Directory containing student submissions.")
    parser.add_argument("-o", type=str, help="Directory to save output files (required if -d is used).")
    parser.add_argument("-m", type=str, help="The file of student names who passed the previous tests.")
    parser.add_argument("-f", type=str, help="Run a single student file instead of a directory.")
    parser.add_argument("-r", "--rename", action="store_true", help="Rename files to student's name.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output.")
    args = parser.parse_args()

    # check necessary arguments
    if args.d:
        # multiple file checking
        if not args.o:
            parser.error("Output directory (-o) is required when processing a directory (-d).")
    else:
        # single file checking
        if not args.f:
            parser.error("Either -d (directory) or -f (single file) must be provided.")

    # create the checker instance
    checker = StudentCodeRunner(
        submission_dir=args.d if args.d else os.path.dirname(args.f),
        output_dir=args.o if args.o else "",  # output directory is not needed for a single file
        run_test=run_test,
        verbose=args.verbose,
        rename=args.rename
    )

    if args.f:
        # single file checking
        print(f"\nRunning single file: {args.f}\n" + "=" * 50)
        student_file = os.path.basename(args.f)
        checker.process_submission(student_file=student_file, current=0, single_file=True)
        print("\nTest Results:")
        print("\n".join(checker.error_logs) if checker.error_logs else f"{student_file} passed!")
    else:
        # multiple fiel checking
        checker.run()


if __name__ == "__main__":
    main()

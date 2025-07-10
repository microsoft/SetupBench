"""
evaluation_harness.py
================

Verifies that a benchmark task completed its setup task successfully.

The script expects a metadata JSON file to be shipped with each benchmark task.
This file should define:
- `success_command`: a shell command verifying the setup success.
- `task_type`: One of the 4 task types, which determines how the success is evaluated.

Additional command-line flags let you override defaults such as the working
directory, output path, or whether a new session is started.

Typical usage:
```bash
python evaluation_harness.py metadata.json \
    --workdir /testbed \
    --output /testbed/_output_/test_results.json \
    --verbose
```

The result file is a tiny JSON blob, e.g. `{"success": true}`.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Literal


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Evaluate whether a benchmark task finished its setup.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required
    p.add_argument(
        "metadata_path",
        type=Path,
        help="Path to the task's metadata JSON file",
    )

    # Common overrides
    expected_workdir = Path("/testbed")

    p.add_argument(
        "-w",
        "--workdir",
        type=Path,
        default=expected_workdir,
        help="Directory in which to run the success command",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=expected_workdir / "_output_" / "test_results.json",
        help="Destination for the JSON results file",
    )
    p.add_argument(
        "-c",
        "--command",
        metavar="CMD",
        required=False,
        default=None,
        help="Override metadata's success_command",
    )

    # Behaviour toggles
    p.add_argument(
        "-n",
        "--new-session",
        action="store_true",
        help="Run the command in a new process session (overrides metadata)",
    )
    p.add_argument(
        "-q",
        "--quiet",
        dest="verbose",
        action="store_false",
        help="Suppress informational output",
    )
    p.set_defaults(verbose=True)

    return p


def load_metadata(path: Path) -> dict:
    """Read and return the JSON metadata file."""
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        sys.exit(f"❌ Metadata file not found: {path}\n{exc}")
    except json.JSONDecodeError as exc:
        sys.exit(f"❌ Invalid JSON in metadata file: {path}\n{exc}")


def run_command(
    command: str,
    cwd: Path,
    start_new_session: bool = False,
    verbose: bool = False,
) -> tuple[str, int]:
    """Execute *command* in *cwd* and return (combined_output, exit_code)."""
    if verbose:
        print(f"🚀 Running command in {cwd}:\n{command}\n")

    proc = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        text=True,
        capture_output=True,
        start_new_session=start_new_session,
    )

    full_output = proc.stdout + proc.stderr
    if verbose:
        print("──────── Command output ────────")
        print(full_output.rstrip() or "[no output]")
        print("────────────────────────────────\n")

    return full_output, proc.returncode


def decide_success(
    task_type: str | None,
    exit_code: int,
    output: str,
) -> dict[Literal["success"], bool]:
    """Return ``{"success": bool}`` based on task-type rules."""
    if task_type == "dependency_resolution":
        return {"success": exit_code == 0}

    return {"success": "Setup successful" in output}


def write_results(results: dict, path: Path, verbose: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(results, f)
    if verbose:
        print(f"✅ Results written to {path}: {results}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    metadata = load_metadata(args.metadata_path)

    success_cmd: str | None = args.command or metadata.get("success_command")
    if not success_cmd:
        parser.error(
            "No success command provided (missing in metadata and not overridden)"
        )

    task_type: str | None = metadata.get("task_type")
    if task_type is None:
        parser.error(
            "No task type specified in metadata (required for success evaluation)"
        )

    start_new_session: bool = (
        args.new_session
        if args.new_session
        else metadata.get("start_new_session", False)
    )

    if args.verbose:
        print(f"📋 Task type: {task_type}")
        print(f"📂 Working directory: {args.workdir}")
        print(f"🗄️  Output file: {args.output}")
        print(f"🔄 New session: {start_new_session}\n")

    # Run and evaluate
    output, exit_code = run_command(
        success_cmd,
        cwd=args.workdir,
        start_new_session=start_new_session,
        verbose=args.verbose,
    )
    results = decide_success(task_type, exit_code, output)

    write_results(results, args.output, verbose=args.verbose)


if __name__ == "__main__":
    main()

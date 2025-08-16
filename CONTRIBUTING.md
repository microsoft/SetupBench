## Contributing to SetupBench

We welcome community contributions that improve the quality, coverage, and reproducibility of SetupBench. Before opening an issue or pull request, please read the guidelines below.

### Ways to Contribute
* Report benchmark inaccuracies (e.g. a success command with false positives, missing prerequisite in a problem statement).
* Propose new scenario instances (must follow the schema and add clear real-world motivation).
* Improve documentation, metadata, or evaluation utilities.
* Add lightweight validation scripts (must not add heavy dependencies).

### Ground Rules
* Keep tasks deterministic. Success commands must be idempotent and not depend on external flaky services.
* Avoid adding network-heavy artifacts (large binary dumps, >5MB each) unless essential.
* Do not include proprietary or non-redistributable content.
* Use UTF-8, LF endings, and POSIX-compliant shell where possible.

### Scenario Schema (JSONL)
Each line represents one instance with at minimum:
```
{
  "instance_id": "string (unique, folder-friendly)",
  "task_type": "bgsetup | dbsetup | dependency_resolution | reposetup",
  "success_command": "shell one-liner producing 'Setup successful' on success",
  "problem_statement": "Natural language task description",
  "base_image": "Container base image identifier",
  "image_tag": "Canonical tag for produced image"
  // Optional fields: notes, description, ecosystem, repo_url, base_commit,
  // language, license_spdx, start_new_session, build_commands,
  // human_actions_lower_bound, human_actions_upper_bound
}
```

### Adding / Updating Fixtures
Place any required fixture under `setupbench/fixtures/<instance_id>/`. Keep them minimal; prefer compressed SQL or BSON dumps where appropriate.

### Validation Checklist Before PR
* `python setupbench/evaluation_harness.py --help` works (no syntax errors).
* Added instances: line count increase acknowledged in README statistics.
* Each new instance has a unique `instance_id` and a matching fixture directory (if required).
* `success_command` exits 0 and echoes `Setup successful` on success, and echoes `Setup failed` (non-zero ok) otherwise.

### Development Environment
No complex build is required. Python 3.11+ recommended for local utilities. Avoid adding dependencies unless strictly necessary.

### License
By contributing you agree your contributions are licensed under the repository's MIT License.

Thank you for helping advance rigorous evaluation of software engineering agents!

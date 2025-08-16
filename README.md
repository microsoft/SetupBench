# SetupBench

Official dataset repository for **[SetupBench: Assessing Software Engineering Agents' Ability to Bootstrap Development Environments](https://arxiv.org/abs/2507.09063)**.

SetupBench isolates a critical but under-evaluated capability of software engineering agents: bootstrapping a fresh development environment from a bare OS image. Agents must install system & language toolchains, resolve dependency conflicts, initialize databases, and configure background / multi-service workloads using only natural language task descriptions plus minimal scaffolding.

## Contents

| Category | File | Instances |
|----------|------|-----------|
| Background service setup | `setupbench/scenarios/background_service_setup.jsonl` | 8 |
| Database setup | `setupbench/scenarios/database_setup.jsonl` | 15 |
| Dependency resolution | `setupbench/scenarios/dependency_resolution.jsonl` | 16 |
| Repository setup & build | `setupbench/scenarios/repo_setup.jsonl` | 54 |
| **Total** | | **93** |

Fixtures required for some instances live under `setupbench/fixtures/<instance_id>/`.

## Data Format (JSONL Schema)
Each scenario file is JSON Lines; one JSON object per line. Core fields:

* `instance_id` (string, unique) – Identifier; if a fixture is needed it matches a directory in `setupbench/fixtures/`.
* `task_type` (enum) – One of `bgsetup`, `dbsetup`, `dependency_resolution`, `reposetup`.
* `success_command` (string) – Shell one-liner run inside `/testbed`; must print `Setup successful` on success (or run tests / probes accordingly) and something else otherwise.
* `problem_statement` (string) – Natural language instructions with constraints (always begin from minimal Ubuntu 22.04 unless base image specifies otherwise).
* `base_image` (string) – The starting container image for the agent.
* `image_tag` (string) – Canonical tag for the final image produced by an external execution harness.

Optional fields extend certain categories: `notes`, `description`, `repo_url`, `base_commit`, `ecosystem`, `language`, `license_spdx`, `start_new_session`, `build_commands`, `human_actions_lower_bound`, `human_actions_upper_bound`.

### Success Semantics
The provided `success_command` is executed after the agent run inside `/testbed`. For `dependency_resolution` tasks we treat **exit code 0** as success; for all others, the harness looks for the substring `Setup successful` in combined stdout+stderr.

## Evaluation Harness
The lightweight harness `setupbench/evaluation_harness.py` loads a metadata JSON (you can construct one mirroring instance fields) and executes the success command, producing a JSON result:

```
python setupbench/evaluation_harness.py metadata.json \
	--workdir /testbed \
	--output /testbed/_output_/test_results.json \
	--verbose
```

Result file example: `{"success": true}`.

Arguments:
* `metadata_path` – JSON file containing at least `success_command` and `task_type`.
* `--command` – Override the encoded success command.
* `--new-session` – Force a new process session (otherwise can be specified in metadata via `start_new_session`).
* `--workdir` – Directory to execute in (default `/testbed`).
* `--output` – Destination for result JSON.
* `--quiet` – Suppress verbose logs.

## Using the Dataset in Your Own Benchmarking
1. Select scenario line(s) from the appropriate JSONL file.
2. If a matching fixture directory exists, copy its contents into `/testbed/` before starting the agent (maintain original filenames and relative paths).
3. Launch the agent with the `problem_statement` prompt and base image.
4. After the agent finishes, run the `success_command` (or call the harness) to record success.
5. Persist logs and timing metrics externally—no persistent state is written by the dataset itself besides fixtures.

### Fixture Loading Rules
* Background services: 6 of 8 scenarios require copying their fixture directory (Gunicorn / NGINX / Celery / file watcher / multiprocess, etc.).
* Database setup: All 15 scenarios have fixtures; some have a `prerunner-<instance_id>` script you must execute before the agent begins to modify initial environment state (e.g., port blocking, corrupted dumps).
* Repo / dependency tasks: No fixture copy—repos are cloned according to `repo_url` & optional `base_commit` into `/testbed` (the repo root becomes `/testbed`).

## Citation
If you use SetupBench, please cite:

```
@article{setupbench2025,
	title={SetupBench: Assessing Software Engineering Agents' Ability to Bootstrap Development Environments},
	author={Arora, Avi and Jang, Jinu and Zilouchian Moghaddam, Roshanak},
	journal={arXiv preprint arXiv:2507.09063},
	year={2025}
}
```

You can also use the `CITATION.cff` file for GitHub's citation panel.

## Contributing
See `CONTRIBUTING.md` for guidelines, schema, and validation checklist.

## License
This repository is released under the MIT License (see `LICENSE`). Scenario data and fixtures are provided for research & benchmarking purposes. Ensure compliance with the upstream OSS licenses of any referenced repositories.

## Security
Security reporting information is in `SECURITY.md`.

## Disclaimer
The dataset includes commands that start services, compile software, or manipulate databases. Execute inside isolated containers or sandboxes. No warranty is provided; use at your own risk.

## Task Category Instructions (Operational Summary)

In general all scenarios provide you the following fields:
- `instance_id`: Identifier to correlate your different artifact with.
- `success_command`: One-liner bash script that can verify task success.
- `base_image`: The base image your LLM Agent should be given.
- `image_tag`: Tag the final output image should have.
- `problem_statement`: The prompt to be passed to your LLM Agent.

The general procedure is to launch your agent on `base_image` with the `problem_statement`, optionally copy any required fixture into `/testbed/`, let it perform actions, then run the `success_command` (or harness) at the end.
Certain tasks require extra steps described below.

### Background Service Setup

For 6 out of the 8 scenarios in the background service setup task, a corresponding fixture need be loaded into `/testbed/` of the image.
Use the `instance_id` to look for a folder of the same name under `setupbench/fixtures/` and copy the contents on to the image.

### Database Setup

All 15 scenarios in the database setup task have a corresponding fixture that need to be loaded into `/testbed/` of the image.
Use the `instance_id` to look for a folder of the same name under `setupbench/fixtures/` and copy the contents on to the image.

5 scenarios, `dbsetup-mongodb-3`, `dbsetup-mysql-3`, `dbsetup-postgresql-3`, `dbsetup-redis-3`, and `dbsetup-sqlite-3`, have a prerunner script that need to be executed to alter the state of the environment before the Agent run begins.

### Dependency Resolution

The `repo_url` and `base_commit` are always provided. The `repo_url` is always an open sourced GitHub repository which should be cloned into `/testbed`/ of the `base_image` at the specified `base_commit`.

### Repo Setup

The `repo_url` is always provided, and some also provide the `base_commit`. The `repo_url` is always an open sourced GitHub repository which should be cloned into `/testbed`/ of the image.
If `base_commit` is provided, make sure to checkout the correct commit.

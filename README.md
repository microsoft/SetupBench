# Setup Bench
This is the official repository for **[SetupBench: Assessing Software Engineering Agents' Ability to Bootstrap Development Environments](https://arxiv.org/abs/2507.09063)**.

## Instructions per Task

In general all scenarios provide you the following:
- `instance_id`: Identifier to correlate your different artifact with.
- `success_command`: One-liner bash script that can verify task success.
- `base_image`: The base image your LLM Agent should be given.
- `image_tag`: Tag the final output image should have.
- `problem_statement`: The prompt to be passed to your LLM Agent.

The general rule of thumb is to spin up your LLM Agent on the `base_image`, with the `problem_statement`, and to run `success_command` at the end of the Agent life cycle.
However certain tasks require extra steps.

### Background Service Setup

For 6 out of the 8 scenarios in the background service setup task, a corresponding fixture need be loaded into `/testbed/` of the image.
Use the `instance_id` to look for a folder of the same name under `setupbench/fixtures/` and copy the contents on to the image.

### Database Setup

All 15 scenarios in the database setup task have a corresponding fixture that need to be loaded into `/testbed/` of the image.
Use the `instance_id` to look for a folder of the same name under `setupbench/fixtures/` and copy the contents on to the image.

5 scenarios, `dbsetup-mongodb-3`, `dbsetup-mysql-3`, `dbsetup-postgresql-3`, `dbsetup-redis-3`, and `dbsetup-sqlite-3`, have a prerunner script that need to be executed to alter the state of the environment before the Agent run begins.

### Dependency Resolution

### Repo Setup

The `repo_url` is always provided, and some also provide the `base_commit`. The `repo_url` is always an open sourced GitHub repository which should be cloned into `/testbed`/ of the image.
If `base_commit` is provided, make sure to checkout the correct commit.

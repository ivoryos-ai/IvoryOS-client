## v0.2.11
- add `wait` to `execute_task` (default `True`): wait for the task and return its output, or `wait=False` to return the task id right away
- `execute_task` no longer modifies the caller's `kwargs` dict
- `run_workflow_kwargs` without kwargs no longer raises a server error; use `run_workflow_repeat` for workflows without parameters
- document `wait`, `get_task_status` and `wait_for_task`; update example

## v0.2.10
- requires IvoryOS >=1.6.2
- add `get_task_status`
- add `get_queue` and `get_last_workflow_run_id`
- fix workflow repeat payload
- add workflow data example

## v0.2.9
- add `get_optimizer_schema`

## v0.2.8
- refactor run campaign to support optimizer-agnostic workflows

## v0.2.7
- support decorator function call

## v0.2.6
- fix endpoint, remove api backdoor

## v0.2.5
- fix submit workflow endpoint

## v0.2.4
- update endpoints after IvoryOS endpoint refactor

## v0.2.3
- exception import

## v0.2.2
- change route for IvoryOS refactor
- change url for IvoryOS v1.1

## v0.2.1
- remove output type

## v0.2.0
- refactoring ivoryos client

## v0.1.2

- Add error handling for ivoryOS not running
- Add return in generated code

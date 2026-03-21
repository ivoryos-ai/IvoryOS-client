import time

from ivoryos_client.client import IvoryosClient

if __name__ == '__main__':
    # todo ensure you first launch the abstract sdl example from the ivoryos project
    #  https://gitlab.com/heingroup/ivoryos at community/examples/abstract_sdl_example/abstract_sdl.py then
    #  in the interface go to the design tab and import the example workflow provided at
    #  community/examples/abstract_sdl_example/example_workflow.json and save it to the library with the name
    #  example_workflow. this will be an example workflow that we run

    client = IvoryosClient(
        url="http://localhost:8000/ivoryos",
        username="admin",
        password="admin",
        # timeout=None # todo add in later? if none, wait for tasks to finish execution, if provided then error if task doesnt finish within the timeout time
    )

    print('basic calls')
    platform_info = client.get_platform_info()
    print(platform_info)
    execution_status = client.get_execution_status()
    print(execution_status)

    # ------------------

    print('example execute task, you will see in the ivoryOS interface compile/run tab logging panel that it will '
          'run the following task, and the execution will wait for the task to finish')
    response = client.execute_task(component='deck.sdl',
                                   method='dose_solvent',
                                   kwargs={'solvent_name': 'Ethanol',
                                           'amount_in_ml': '2.5',
                                           'rate_ml_per_minute': '3.5',
                                           })
    print(response)

    # ------------------

    print('example load workflow, load the provided example workflow saved to the library')
    client.load_workflow_script(workflow_name='example_workflow')

    print('execute loaded workflow 4 times split into batches of 2 with specific parameters')
    response = client.run_workflow_kwargs(kwargs_list=[{'param_1': '1',  # run 1 - batch 1 repeat 1
                                                        'param_2': '1',
                                                        },
                                                       {'param_1': '2',  # run 2 - batch 1 repeat 2
                                                        'param_2': '2',
                                                        },
                                                       {'param_1': '3',  # run 3 - batch 2 repeat 1
                                                        'param_2': '3',
                                                        },
                                                       {'param_1': '4',  # run 4 - batch 2 repeat 2
                                                        'param_2': '4',
                                                        },
                                                       ],
                                          batch_size=2,
    )
    print(response)
    last_workflow_run_id = client.get_last_workflow_run_id()
    print(f'last workflow run id: {last_workflow_run_id}')

    print('check execution status before workflow finishes running and wait for execution to finish')
    execution_status = client.get_execution_status()
    print(execution_status)
    is_execution_status_busy = execution_status['busy']
    while is_execution_status_busy:
        time.sleep(1)
        execution_status = client.get_execution_status()
        print(execution_status)
        is_execution_status_busy = execution_status['busy']
    print('execution status is not busy, workflow has finished running')

    last_workflow_data = client.load_workflow_data(workflow_id=last_workflow_run_id)
    print('last workflow run data')
    print(last_workflow_data)
    print(f'csv data saved at: {last_workflow_data["csv_file_name"]}')

    print(f'showing outputs from main experiment phase for workflow id: {last_workflow_run_id}')
    experiment_run_iteration_data = last_workflow_data['phases']['script']  # key: value of iteration_name: data
    iteration_names = list(last_workflow_data['phases']['script'].keys())
    for iteration_name in iteration_names:
        iteration_data = experiment_run_iteration_data[iteration_name][0] # has to be first item in list, not sure when there will be more in the list?
        iteration_parameters = iteration_data['parameters'] # list of dict, where index in list is the batch index for the iteration
        iteration_outputs = iteration_data['outputs'] # list of dict, where index in list is the batch index for the iteration
        for batch_index in range(len(iteration_outputs)):
            print(f'iteration name: {iteration_name}, batch index: {batch_index}\n'
                  f'    iteration parameters: {iteration_parameters[batch_index]}\n'
                  f'    iteration outputs: {iteration_outputs[batch_index]}')

    """
    Example print output from running this
    
    basic calls
    workflow execution has 3 blocks, prep, main (iterate) and cleanup.
    one can execute the workflow using one of the 3 options:
    1. simple repeat for static workflow with `run_workflow_repeat`
    2. repeat with kwargs `run_workflow_kwargs`
    3. campaign `run_workflow_campaign`
    Available functions: {'deck.balance': {'dose_solid': {'coroutine': False, 'docstring': 'this function is used to dose solid', 'has_args': False, 'has_kwargs': False, 'signature': '(self, amount_in_mg: float)'}, 'setter_value': {'coroutine': False, 'docstring': None, 'has_setter': True, 'is_property': True, 'signature': '(self)'}, 'weigh_sample': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self)'}}, 'deck.pump': {'dose_liquid': {'coroutine': False, 'docstring': 'dose liquid', 'has_args': False, 'has_kwargs': False, 'signature': '(self, amount_in_ml: float, rate_ml_per_minute: float = 1)'}}, 'deck.sdl': {'analyze': {'coroutine': False, 'docstring': 'analyze current chemical', 'has_args': False, 'has_kwargs': False, 'signature': '(self, param_1: int, param_2: int)'}, 'dose_solid': {'coroutine': False, 'docstring': 'dose current chemical', 'has_args': False, 'has_kwargs': False, 'signature': "(self, amount_in_mg: float = 5, solid_name: str = 'acetaminophen')"}, 'dose_solvent': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': "(self, solvent_name: Optional[community.solvent.Solvent] = <Solvent.Methanol: 'Methanol'>, amount_in_ml: float = 5, rate_ml_per_minute: float = 1)"}, 'equilibrate': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self, temp: float, duration: float)'}, 'fn_with_list': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self, list_arg: List[str])'}, 'get_dummy_input': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self, i: int) -> int'}, 'get_solvent': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self) -> community.solvent.Solvent'}, 'optional_str': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self, solvent: Optional[str] = None)'}, 'raise_runtime_error': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self)'}, 'raise_timeout_error': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self)'}, 'return_random_int': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self) -> int'}, 'use_solvent': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self, solvent: community.solvent.Solvent)'}}}
    {'busy': False, 'current_task': {}, 'workflow_status': {'runner_status': {'is_running': False, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-51-01.csv', 'end_time': 'Fri, 20 Mar 2026 19:51:17 GMT', 'id': 494, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:51:01 GMT'}}}
    example execute task, you will see in the ivoryOS interface compile/run tab logging panel that it will run the following task, and the execution will wait for the task to finish
    {'status': 'task started', 'task_id': 38}
    example load workflow, load the provided example workflow saved to the library
    execute loaded workflow 4 times split into batches of 2 with specific parameters
    {'status': 'task started', 'task_id': 38}
    last workflow run id: 495
    check execution status before workflow finishes running and wait for execution to finish
    {'busy': True, 'current_task': {'end_time': None, 'id': 1359, 'method_name': 'wait', 'output': {}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1359, 'method_name': 'wait', 'output': {}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1359, 'method_name': 'wait', 'output': {}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1360, 'method_name': 'wait', 'output': {}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:23 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1360, 'method_name': 'wait', 'output': {}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:23 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1360, 'method_name': 'wait', 'output': {}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:23 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1361, 'method_name': 'analyze', 'output': {}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:26 GMT', 'step_index': 2}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1362, 'method_name': 'analyze', 'output': {}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:27 GMT', 'step_index': 2}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1365, 'method_name': 'wait', 'output': {}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1365, 'method_name': 'wait', 'output': {}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1365, 'method_name': 'wait', 'output': {}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1366, 'method_name': 'wait', 'output': {}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:32 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1366, 'method_name': 'wait', 'output': {}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:32 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1366, 'method_name': 'wait', 'output': {}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:32 GMT', 'step_index': 1}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1367, 'method_name': 'analyze', 'output': {}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:35 GMT', 'step_index': 2}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 1368, 'method_name': 'analyze', 'output': {}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:36 GMT', 'step_index': 2}, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': None, 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    {'busy': False, 'current_task': {}, 'workflow_status': {'runner_status': {'is_running': False, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}}
    execution status is not busy, workflow has finished running
    last workflow run data
    {'csv_file_name': 'example_workflow_2026-03-20 19-52-20.csv', 'phases': {'cleanup': [{'end_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'id': 1283, 'name': 'cleanup', 'outputs': [{}], 'parameters': None, 'repeat_index': 0, 'run_id': 495, 'start_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'steps': []}], 'prep': [{'end_time': 'Fri, 20 Mar 2026 19:52:20 GMT', 'id': 1280, 'name': 'prep', 'outputs': [{}], 'parameters': None, 'repeat_index': 0, 'run_id': 495, 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT', 'steps': []}], 'script': {'0': [{'end_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'id': 1281, 'name': 'main', 'outputs': [{'analyze_result': 0.8237634240234676, 'param_1': '1', 'param_2': '1'}, {'analyze_result': 0.7964910305837648, 'param_1': '2', 'param_2': '2'}], 'parameters': [{'param_1': '1', 'param_2': '1'}, {'param_1': '2', 'param_2': '2'}], 'repeat_index': 0, 'run_id': 495, 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT', 'steps': [{'end_time': 'Fri, 20 Mar 2026 19:52:23 GMT', 'id': 1359, 'method_name': 'wait', 'output': {'param_1': '1', 'param_2': '1'}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT', 'step_index': 1}, {'end_time': 'Fri, 20 Mar 2026 19:52:26 GMT', 'id': 1360, 'method_name': 'wait', 'output': {'param_1': '2', 'param_2': '2'}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:23 GMT', 'step_index': 1}, {'end_time': 'Fri, 20 Mar 2026 19:52:27 GMT', 'id': 1361, 'method_name': 'analyze', 'output': {'analyze_result': 0.8237634240234676, 'param_1': '1', 'param_2': '1'}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:26 GMT', 'step_index': 2}, {'end_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'id': 1362, 'method_name': 'analyze', 'output': {'analyze_result': 0.7964910305837648, 'param_1': '2', 'param_2': '2'}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:27 GMT', 'step_index': 2}, {'end_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'id': 1363, 'method_name': 'comment', 'output': {'analyze_result': 0.8237634240234676, 'param_1': '1', 'param_2': '1'}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'step_index': 3}, {'end_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'id': 1364, 'method_name': 'comment', 'output': {'analyze_result': 0.7964910305837648, 'param_1': '2', 'param_2': '2'}, 'phase_id': 1281, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'step_index': 3}]}], '1': [{'end_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'id': 1282, 'name': 'main', 'outputs': [{'analyze_result': 0.08447447713674594, 'param_1': '3', 'param_2': '3'}, {'analyze_result': 0.7340939277730789, 'param_1': '4', 'param_2': '4'}], 'parameters': [{'param_1': '3', 'param_2': '3'}, {'param_1': '4', 'param_2': '4'}], 'repeat_index': 1, 'run_id': 495, 'start_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'steps': [{'end_time': 'Fri, 20 Mar 2026 19:52:32 GMT', 'id': 1365, 'method_name': 'wait', 'output': {'param_1': '3', 'param_2': '3'}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:29 GMT', 'step_index': 1}, {'end_time': 'Fri, 20 Mar 2026 19:52:35 GMT', 'id': 1366, 'method_name': 'wait', 'output': {'param_1': '4', 'param_2': '4'}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:32 GMT', 'step_index': 1}, {'end_time': 'Fri, 20 Mar 2026 19:52:36 GMT', 'id': 1367, 'method_name': 'analyze', 'output': {'analyze_result': 0.08447447713674594, 'param_1': '3', 'param_2': '3'}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:35 GMT', 'step_index': 2}, {'end_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'id': 1368, 'method_name': 'analyze', 'output': {'analyze_result': 0.7340939277730789, 'param_1': '4', 'param_2': '4'}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:36 GMT', 'step_index': 2}, {'end_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'id': 1369, 'method_name': 'comment', 'output': {'analyze_result': 0.08447447713674594, 'param_1': '3', 'param_2': '3'}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'step_index': 3}, {'end_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'id': 1370, 'method_name': 'comment', 'output': {'analyze_result': 0.7340939277730789, 'param_1': '4', 'param_2': '4'}, 'phase_id': 1282, 'run_error': False, 'start_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'step_index': 3}]}]}}, 'workflow_info': {'data_path': 'example_workflow_2026-03-20 19-52-20.csv', 'end_time': 'Fri, 20 Mar 2026 19:52:37 GMT', 'id': 495, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Fri, 20 Mar 2026 19:52:20 GMT'}}
    csv data saved at: example_workflow_2026-03-20 19-52-20.csv
    showing outputs from main experiment phase for workflow id: 495
    iteration name: 0, batch index: 0
        iteration parameters: {'param_1': '1', 'param_2': '1'}
        iteration outputs: {'analyze_result': 0.8237634240234676, 'param_1': '1', 'param_2': '1'}
    iteration name: 0, batch index: 1
        iteration parameters: {'param_1': '2', 'param_2': '2'}
        iteration outputs: {'analyze_result': 0.7964910305837648, 'param_1': '2', 'param_2': '2'}
    iteration name: 1, batch index: 0
        iteration parameters: {'param_1': '3', 'param_2': '3'}
        iteration outputs: {'analyze_result': 0.08447447713674594, 'param_1': '3', 'param_2': '3'}
    iteration name: 1, batch index: 1
        iteration parameters: {'param_1': '4', 'param_2': '4'}
        iteration outputs: {'analyze_result': 0.7340939277730789, 'param_1': '4', 'param_2': '4'}
        
    """
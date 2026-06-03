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
        timeout=None
    )

    print('basic calls')
    platform_info = client.get_platform_info()
    print(platform_info)
    execution_status = client.get_execution_status()
    print(execution_status)
    execution_queue = client.get_queue()
    print(execution_queue)

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
    task_id = response['task_id']
    print(f'task status for workflow id: {task_id}')
    task_status_data = client.get_task_status(task_id)
    print(task_status_data)

    # ------------------

    print('example load workflow, load the provided example workflow saved to the library')
    client.load_workflow_script(workflow_name='example_workflow')

    print('execute loaded workflow 4 times split into batches of 2 with specific parameters')
    response = client.run_workflow_kwargs(kwargs_list=[{'param_1': '1',  # run 1 - iteration 1 batch 1
                                                        'param_2': '1',
                                                        },
                                                       {'param_1': '2',  # run 2 - iteration 1 batch 2
                                                        'param_2': '2',
                                                        },
                                                       {'param_1': '3',  # run 3 - iteration 2 batch 1
                                                        'param_2': '3',
                                                        },
                                                       {'param_1': '4',  # run 4 - iteration 2 batch 2
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
        iteration_data = experiment_run_iteration_data[iteration_name][
            0]  # has to be first item in list, not sure when there will be more in the list?
        iteration_parameters = iteration_data[
            'parameters']  # list of dict, where index in list is the batch index for the iteration
        iteration_outputs = iteration_data[
            'outputs']  # list of dict, where index in list is the batch index for the iteration
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
    Available functions: {'deck.balance': {'dose_solid': {'coroutine': False, 'docstring': 'this function is used to dose solid', 'has_args': False, 'has_kwargs': False, 'signature': '(self, amount_in_mg: float)'}, 'setter_value': {'coroutine': False, 'docstring': None, 'has_setter': True, 'is_property': True, 'signature': '(self)'}, 'weigh_sample': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self)'}}, 'deck.pump': {'dose_liquid': {'coroutine': False, 'docstring': 'dose liquid', 'has_args': False, 'has_kwargs': False, 'signature': '(self, amount_in_ml: float, rate_ml_per_minute: float = 1)'}}, 'deck.sdl': {'analyze': {'coroutine': False, 'docstring': 'analyze current chemical', 'has_args': False, 'has_kwargs': False, 'signature': '(self, param_1: int, param_2: int)'}, 'dose_solid': {'coroutine': False, 'docstring': 'dose current chemical', 'has_args': False, 'has_kwargs': False, 'signature': "(self, amount_in_mg: float = 5, solid_name: str = 'acetaminophen')"}, 'dose_solvent': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self, solvent_name: Optional[__main__.Solvent] = None, amount_in_ml: float = 5, rate_ml_per_minute: float = 1)'}, 'equilibrate': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self, temp: float, duration: float)'}, 'simulate_error': {'coroutine': False, 'docstring': None, 'has_args': False, 'has_kwargs': False, 'signature': '(self)'}}}
    {'busy': False, 'current_task': {'end_time': 'Wed, 03 Jun 2026 12:06:38 GMT', 'id': 53, 'kwargs': {'amount_in_ml': '2.5', 'rate_ml_per_minute': '3.5', 'solvent_name': 'Ethanol'}, 'method_name': 'deck.sdl.dose_solvent', 'output': 1, 'run_error': None, 'start_time': 'Wed, 03 Jun 2026 12:06:36 GMT'}, 'paused': False}
    []
    example execute task, you will see in the ivoryOS interface compile/run tab logging panel that it will run the following task, and the execution will wait for the task to finish
    {'status': 'task started', 'task_id': 54}
    task status for workflow id: 54
    {'end_time': 'Wed, 03 Jun 2026 12:06:51 GMT', 'id': 54, 'kwargs': {'amount_in_ml': '2.5', 'rate_ml_per_minute': '3.5', 'solvent_name': 'Ethanol'}, 'method_name': 'deck.sdl.dose_solvent', 'output': 1, 'run_error': None, 'start_time': 'Wed, 03 Jun 2026 12:06:49 GMT'}
    example load workflow, load the provided example workflow saved to the library
    execute loaded workflow 4 times split into batches of 2 with specific parameters
    {'status': 'task started', 'task_id': 54}
    last workflow run id: 607
    check execution status before workflow finishes running and wait for execution to finish
    {'busy': True, 'current_task': {'end_time': None, 'id': 2165, 'method_name': 'wait', 'output': {}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2165, 'method_name': 'wait', 'output': {}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2165, 'method_name': 'wait', 'output': {}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2166, 'method_name': 'wait', 'output': {}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:55 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2166, 'method_name': 'wait', 'output': {}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:55 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2166, 'method_name': 'wait', 'output': {}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:55 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2167, 'method_name': 'analyze', 'output': {}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:58 GMT', 'step_index': 2}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2168, 'method_name': 'analyze', 'output': {}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:59 GMT', 'step_index': 2}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2171, 'method_name': 'wait', 'output': {}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2171, 'method_name': 'wait', 'output': {}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2171, 'method_name': 'wait', 'output': {}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2172, 'method_name': 'wait', 'output': {}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:03 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2172, 'method_name': 'wait', 'output': {}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:03 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2172, 'method_name': 'wait', 'output': {}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:03 GMT', 'step_index': 1}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2173, 'method_name': 'analyze', 'output': {}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:06 GMT', 'step_index': 2}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': True, 'current_task': {'end_time': None, 'id': 2174, 'method_name': 'analyze', 'output': {}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:07 GMT', 'step_index': 2}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': True, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': None, 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    {'busy': False, 'current_task': {}, 'paused': False, 'workflow_status': {'runner_status': {'is_running': False, 'paused': False, 'stop_current': False, 'stop_pending': False}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}}
    execution status is not busy, workflow has finished running
    last workflow run data
    {'csv_file_name': 'example_workflow_2026-06-03 12-06-52.csv', 'phases': {'cleanup': [{'end_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'id': 1726, 'name': 'cleanup', 'outputs': [{}], 'parameters': None, 'repeat_index': 1, 'run_id': 607, 'start_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'steps': []}], 'prep': [{'end_time': 'Wed, 03 Jun 2026 12:06:52 GMT', 'id': 1723, 'name': 'prep', 'outputs': [{}], 'parameters': None, 'repeat_index': 1, 'run_id': 607, 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT', 'steps': []}], 'script': {'1': [{'end_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'id': 1724, 'name': 'main', 'outputs': [{'analyze_result': 0.3663028670854228, 'param_1': '1', 'param_2': '1'}, {'analyze_result': 0.47924161593228143, 'param_1': '2', 'param_2': '2'}], 'parameters': [{'param_1': '1', 'param_2': '1'}, {'param_1': '2', 'param_2': '2'}], 'repeat_index': 1, 'run_id': 607, 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT', 'steps': [{'end_time': 'Wed, 03 Jun 2026 12:06:55 GMT', 'id': 2165, 'method_name': 'wait', 'output': {'param_1': '1', 'param_2': '1'}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT', 'step_index': 1}, {'end_time': 'Wed, 03 Jun 2026 12:06:58 GMT', 'id': 2166, 'method_name': 'wait', 'output': {'param_1': '2', 'param_2': '2'}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:55 GMT', 'step_index': 1}, {'end_time': 'Wed, 03 Jun 2026 12:06:59 GMT', 'id': 2167, 'method_name': 'analyze', 'output': {'analyze_result': 0.3663028670854228, 'param_1': '1', 'param_2': '1'}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:58 GMT', 'step_index': 2}, {'end_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'id': 2168, 'method_name': 'analyze', 'output': {'analyze_result': 0.47924161593228143, 'param_1': '2', 'param_2': '2'}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:06:59 GMT', 'step_index': 2}, {'end_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'id': 2169, 'method_name': 'comment', 'output': {'analyze_result': 0.3663028670854228, 'param_1': '1', 'param_2': '1'}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'step_index': 3}, {'end_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'id': 2170, 'method_name': 'comment', 'output': {'analyze_result': 0.47924161593228143, 'param_1': '2', 'param_2': '2'}, 'phase_id': 1724, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'step_index': 3}]}], '2': [{'end_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'id': 1725, 'name': 'main', 'outputs': [{'analyze_result': 0.3740858297547359, 'param_1': '3', 'param_2': '3'}, {'analyze_result': 0.3895619383016137, 'param_1': '4', 'param_2': '4'}], 'parameters': [{'param_1': '3', 'param_2': '3'}, {'param_1': '4', 'param_2': '4'}], 'repeat_index': 2, 'run_id': 607, 'start_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'steps': [{'end_time': 'Wed, 03 Jun 2026 12:07:03 GMT', 'id': 2171, 'method_name': 'wait', 'output': {'param_1': '3', 'param_2': '3'}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:00 GMT', 'step_index': 1}, {'end_time': 'Wed, 03 Jun 2026 12:07:06 GMT', 'id': 2172, 'method_name': 'wait', 'output': {'param_1': '4', 'param_2': '4'}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:03 GMT', 'step_index': 1}, {'end_time': 'Wed, 03 Jun 2026 12:07:07 GMT', 'id': 2173, 'method_name': 'analyze', 'output': {'analyze_result': 0.3740858297547359, 'param_1': '3', 'param_2': '3'}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:06 GMT', 'step_index': 2}, {'end_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'id': 2174, 'method_name': 'analyze', 'output': {'analyze_result': 0.3895619383016137, 'param_1': '4', 'param_2': '4'}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:07 GMT', 'step_index': 2}, {'end_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'id': 2175, 'method_name': 'comment', 'output': {'analyze_result': 0.3740858297547359, 'param_1': '3', 'param_2': '3'}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'step_index': 3}, {'end_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'id': 2176, 'method_name': 'comment', 'output': {'analyze_result': 0.3895619383016137, 'param_1': '4', 'param_2': '4'}, 'phase_id': 1725, 'run_error': False, 'start_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'step_index': 3}]}]}}, 'workflow_info': {'data_path': 'example_workflow_2026-06-03 12-06-52.csv', 'end_time': 'Wed, 03 Jun 2026 12:07:08 GMT', 'id': 607, 'name': 'example_workflow', 'platform': 'abstract_sdl', 'repeat_mode': 'batch', 'start_time': 'Wed, 03 Jun 2026 12:06:52 GMT'}}
    csv data saved at: example_workflow_2026-06-03 12-06-52.csv
    showing outputs from main experiment phase for workflow id: 607
    iteration name: 1, batch index: 0
        iteration parameters: {'param_1': '1', 'param_2': '1'}
        iteration outputs: {'analyze_result': 0.3663028670854228, 'param_1': '1', 'param_2': '1'}
    iteration name: 1, batch index: 1
        iteration parameters: {'param_1': '2', 'param_2': '2'}
        iteration outputs: {'analyze_result': 0.47924161593228143, 'param_1': '2', 'param_2': '2'}
    iteration name: 2, batch index: 0
        iteration parameters: {'param_1': '3', 'param_2': '3'}
        iteration outputs: {'analyze_result': 0.3740858297547359, 'param_1': '3', 'param_2': '3'}
    iteration name: 2, batch index: 1
        iteration parameters: {'param_1': '4', 'param_2': '4'}
        iteration outputs: {'analyze_result': 0.3895619383016137, 'param_1': '4', 'param_2': '4'}
    """
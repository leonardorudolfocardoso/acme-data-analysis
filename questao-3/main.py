import os
import pandas as pd

cur_path = os.path.dirname(__file__)
data_path = os.path.relpath('../data')
raw_functions = pd.read_csv(os.path.join(data_path, 'functions.csv'))
raw_executions = pd.read_csv(os.path.join(data_path, 'executions.csv'))

print(raw_functions)
print(raw_executions)

# copy dataframe
functions = raw_functions.copy()
executions = raw_executions.copy()

# function to subtract_latency from execution_time
def subtract_latency(df):
    function_id = df['function_id']
    external_component_avg_latency = raw_functions[raw_functions['id'] == function_id]['external_component_avg_latency'].values[0]
    return df['execution_time'] - external_component_avg_latency

executions['execution_time_for_deviation'] = executions[['function_id', 'execution_time']].apply(lambda df: subtract_latency(df), axis=1)

print(executions)

functions_study = pd.DataFrame()

functions_study['execution_time_deviation'] = executions.groupby('function_id').std()['execution_time_for_deviation']

functions_study['execution_time_mean'] = executions.groupby('function_id').mean()['execution_time_for_deviation']

functions_study['execution_time_deviation_porcentage'] = 100*functions_study['execution_time_deviation']/functions_study['execution_time_mean']

print(functions_study)
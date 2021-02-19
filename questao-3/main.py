import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cur_path = os.path.dirname(__file__)
data_path = os.path.relpath('../data')
raw_functions = pd.read_csv(os.path.join(data_path, 'functions.csv'), index_col='id')
raw_executions = pd.read_csv(os.path.join(data_path, 'executions.csv'), index_col='id')

print(raw_functions)
print(raw_executions)

# copy dataframe
functions = raw_functions.copy()
executions = raw_executions.copy()

# sort executions by date
executions.sort_values('date', inplace=True)

# get dictionary to functions latency
functions_latency_dict = functions['external_component_avg_latency'].to_dict()

# subtract latency from execution time
executions['function_execution_time'] = executions[['function_id', 'execution_time']].apply(lambda df: df['execution_time'] - functions_latency_dict[df['function_id']], 1)

# show results
print(executions)

# create dict with execution_time mean
functions_execution_time_mean_dict = executions.groupby('function_id').mean()['function_execution_time'].to_dict()

# show results
print('\nExecution time means: ')
for key in functions_execution_time_mean_dict.keys():
    value = functions_execution_time_mean_dict[key]
    print('\tFunction id {}: {:.0f}'.format(key, value))

# calculate porcentage variation from mean for each execution
executions['variation'] = executions[['function_id', 'function_execution_time']] \
    .apply(lambda df:
        100*np.abs(df['function_execution_time'] - functions_execution_time_mean_dict[df['function_id']])/functions_execution_time_mean_dict[df['function_id']],
        axis=1)

# show results
print(executions)

# create must be optimized
executions['must_be_optimized'] = executions['variation'].apply(lambda variation: variation >= 30)

# print how many times each function time execution variation is greater than 30%
print('Must be optimized count: ')
print(executions[executions['must_be_optimized']][['function_id', 'must_be_optimized']].groupby('function_id').count())

def return_function_condition(boolean: bool):
    if (boolean):
        return 'must be optimized'
    else:
        return 'inside tolerance'

# create function_condition column, which is 'must be optimized' or 'inside tolerance'
executions['function_condition'] = executions['must_be_optimized'].apply(lambda value: return_function_condition(bool(value)))

# show results
print(executions)

# create date time limits
initial_date = executions['date'].values[0]
final_date = executions['date'].values[-1]
date_limits = np.array([initial_date, final_date])

# create graphic
fig, axis = plt.subplots(2, 3, sharex=True, figsize=(12, 12), dpi=300)
axis = [ax for sublist in axis for ax in sublist]

for ax, function_id in zip(axis, functions.sort_index().index.values):
    # get function name
    function_name = functions.loc[function_id]['function_name']

    # plot data
    sns.scatterplot(data=executions[executions['function_id']==function_id], x='date', y='function_execution_time', hue='function_condition', s=25, palette='muted', ax=ax)

    # get and plot mean
    mean = functions_execution_time_mean_dict[function_id]
    ax.plot(date_limits, np.array([mean, mean]), c='g', label='mean', lw=2)

    # calculate limits
    lower_limit = 1.3*np.array([mean, mean])
    upper_limit = 0.7*np.array([mean, mean])

    # plot limits
    ax.plot(date_limits, lower_limit, c='r', label='tolerance limit', lw=2)
    ax.plot(date_limits, upper_limit, c='r', lw=2)

    ax.set_title("Function '{}' (id {})".format(function_name, function_id))
    ax.set_xticks(ax.get_xticks()[::50])
    ax.set_ylabel('t (ms)')
    ax.tick_params(rotation=45)
    # ax.grid()
    ax.legend()

fig.suptitle('Execution time variation over time', weight='bold', size=24)
fig.tight_layout()
fig.subplots_adjust(top=0.93)
fig.savefig('fig.png')
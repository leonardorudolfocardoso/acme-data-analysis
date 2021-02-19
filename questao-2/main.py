import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# define execution cost
EXECUTION_COST = 0.000015

def round_up_by10(number: int, power: int):
    """
        returns number rounded to a specific power of 10
    """
    if not isinstance(power, int):
        raise TypeError('power arg must be an integer')
    elif power < 0:
        raise ValueError('power arg must not be less than 0')

    factor = 10**power
    return factor*np.ceil(number/factor)

def apply_cost(dataframe):
    """
        returns cost with rounded or not rounded execution time according to before_date bool
    """
    if dataframe['before_date']:
        return dataframe['rounded_execution_time'] * EXECUTION_COST
    else:
        return dataframe['execution_time'] * EXECUTION_COST

# import csv data
cur_path = os.path.dirname(__file__)
data_path = os.path.relpath('../data')
raw_functions = pd.read_csv(os.path.join(data_path, 'functions.csv'))
raw_executions = pd.read_csv(os.path.join(data_path, 'executions.csv'))

# show imported data head
# print('Imported dataframes heads\n')
# print(raw_functions.head())
# print()
# print(raw_executions.head())
# print()

# solve executions time and cost
print('Solving executions time and cost...\n')
## copy raw_executions dataframe
executions = raw_executions.copy()
## create new column with rounded execution time
executions['rounded_execution_time'] = executions[['execution_time']].apply(lambda x: round_up_by10(x, 2))

## solve executions cost for condition b (old princing model until 2020-06-13)
print('Solving cost for condition b\n')
date_of_change = '2020-06-13'

### create new column with bool before_date
executions['before_date'] = executions['date'].apply(lambda date: date < date_of_change)

### apply apply_cost function
executions['cost_condition_b'] = executions[ \
        ['execution_time', 'rounded_execution_time', 'before_date']
    ] \
    .apply(lambda df: apply_cost(df), axis=1)
print(executions, '\n')

## solve cost for condition d (old pricing model)
print('Solving cost for condition d\n')
executions['cost_condition_d'] = executions[['rounded_execution_time']]*EXECUTION_COST
print(executions, '\n')

## solve cost for condition e (new pricing model)
print('Solving cost for condition e\n')
executions[['cost_condition_e']] = executions[['execution_time']]*EXECUTION_COST
print(executions, '\n')

## solve cost saving for condition c (cost saving by new pricing model adoption)
print('Solving cost saving for condition c\n')
executions['cost_saving_condition_c'] = executions['cost_condition_d'] - executions['cost_condition_b']
print(executions, '\n')

# gather executions time and cost in a dictionary
cost_conditions = [
    {
        'key': 'cost_condition_b',
        'description': 'old princing model until 2020-06-13'
    },
    {
        'key': 'cost_condition_d', 
        'description': 'old pricing model'
    },
    {
        'key': 'cost_saving_condition_c', 
        'description': 'cost saving by new pricing model adoption'
    },
    {
        'key': 'cost_condition_e',
        'description': 'new pricing model'
    },
]

# print each execution cost
for cost_condition in cost_conditions:
    cost_label = cost_condition['key'].replace('_', ' ')
    print('\tTotal sum in {}: {:.2f} ({})\n'.format(cost_label, executions[cost_condition['key']].sum(), cost_condition['description']))


# sorting dataframe by date
executions.sort_values('date', inplace=True)
# creating cumulative sum for costs
for cost_condition in cost_conditions:
    cost_label = 'cumsum_{}'.format(cost_condition['key'])
    executions[cost_label] = executions[cost_condition['key']].cumsum()

# plots

## plot with different axis
# fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(16, 16))
# axis = [ax1, ax2, ax3, ax4]

# for cost_condition, ax in zip(cost_conditions, axis):
#     cumsum_key = 'cumsum_{}'.format(cost_condition['key'])
#     ax.plot(executions['date'], executions[cumsum_key])
#     ax.set_title('{} over time'.format(cost_condition['key'].replace('_', ' ')))
#     ax.set_xticks(ax.get_xticks()[::80])
#     ax.tick_params(labelrotation=45)
#     ax.grid()

## plot in a unique axe
fig = plt.figure(figsize=(12, 12), dpi=300)
ax = fig.add_subplot(111)

for cost_condition in cost_conditions:
    cumsum_key = 'cumsum_{}'.format(cost_condition['key'])
    plot_label = cost_condition['key'].replace('_', ' ')
    ax.plot(executions['date'], executions[cumsum_key], label=plot_label, lw=1.5)

ax.set_xticks(ax.get_xticks()[::50])
ax.tick_params(rotation=45)
ax.grid()
ax.legend()
ax.set_title('Pricing model cost comparison over time')
ax.set_ylabel('R$')

fig.savefig('fig.png')
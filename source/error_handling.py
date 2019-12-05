

def check_user_assumptions(data):
    usr_ass = data.user_assumptions

    assert all(isinstance(x, int) for x in usr_ass['charging_points_nr']), \
        'Invalid value for number of charging points. Must be integer.'
    assert all(0 < x for x in usr_ass['charging_points_nr']), \
        'Number of charging points must be of type integer and greater than 0.'

    assert all(isinstance(x, (float, int)) for x in usr_ass['power_in_kW']), \
        'Invalid value for input power in kW. Must be float or integer.'
    assert all(0 < x for x in usr_ass['power_in_kW']), \
        'Power in kW must be of type float or integer and greater than 0.'

    assert type(usr_ass['days_per_week']) is float or type(usr_ass['days_per_week']) is int, \
        'Invalid value for input days per week. Must be float or integer'
    assert usr_ass['days_per_week'] <= 7.0, \
        'Days per week must be <= 7.'

    assert type(usr_ass['simulation_time_in_weeks']) is int, \
        'Invalid value for the simulation time in weeks. Must be integer.'

    control_strategy = ['UC', 'DF', 'FCFS', 'WS', 'OPT']
    assert all(x in control_strategy for x in usr_ass['control_strategies']), \
        'Invalid control strategy must be either UC, DF, FCFS, WS or OPT'

    assert all(isinstance(x, (float, int)) for x in usr_ass['storage_capacity']), \
        'Invalid value for input storage capacity. Must be float or integer'

    assert all(isinstance(x, (float, int)) for x in usr_ass['number_of_evs']), \
        'Invalid value for input number of evs. Must be integer'
    assert all(0 < x for x in usr_ass['number_of_evs']), \
        'Number of vehicles must be of type integer and greater than 0.'

    assert all(isinstance(x, (float, int)) for x in usr_ass['cost_weights']), \
        'Invalid value for input cost weights. Must be float or 0 or 1.'
    assert all(0 <= x <= 1 for x in usr_ass['cost_weights']), \
        'Cost weights must be >= 0 and <= 1.'

    assert all(isinstance(x, (float, int)) and 0 <= x < 24 for x in usr_ass['opening_hours']), \
        'Invalid value for input opening hours. Must be float or integer and between 0 and 24 (0 <= hour < 24).'
    assert len(usr_ass['opening_hours']) == 2, \
        'Please only assign 2 values for opening hours. Start and end in hours.'


def check_input_file_cols(cols_input_file, user_inputs, input_name):
    if type(user_inputs) == list:
        assert all(x in cols_input_file for x in user_inputs), \
            'Invalid value for ' + input_name + ". Can't find requested scenario in data file."
    else:
        assert user_inputs in cols_input_file, \
            'Invalid value for ' + input_name + ". Can't find requested scenario in data file."

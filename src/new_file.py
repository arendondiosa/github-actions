def docstring_to_yaml_two(docstring_dict, tab_size=1):
    """
    Transform a docstring in yaml format
    :param docstring_dict: Dict, Docstring Ie,
        {
            "short_description": ...,
            "long_description": ...,
            "params": [{"name": ..., "doc": ..., "example": ..., "type": ...}, ...],
            "returns": ...
        }
    :param tab_size: Integer, Tab size. Ie, 1
    :return String, docstring in yaml format Ie,
        "
        Create lead owners and create lead guarantors person if the client has the property active 
        ---
        parameters:
        - name: client_id
           in: path 
           description: Client identifier.
           required: true
           type: int
           default: 3
        "
    """
    parameters_yaml = ''
    responses_yaml = ''
    yaml = ''
    is_params_enabled = 'params' in docstring_dict and docstring_dict['params']
    is_returns_enabled = 'returns' in docstring_dict and docstring_dict['returns']

    if 'short_description' in docstring_dict and docstring_dict[
            'short_description']:
        yaml += '***' + docstring_dict['short_description']

    if 'long_description' in docstring_dict and docstring_dict[
            'long_description']:
        yaml += '\n***' + docstring_dict['long_description']

    if is_params_enabled or is_returns_enabled:
        yaml += '\n***---'

    if is_params_enabled:
        params = docstring_dict['params']
        parameters_yaml = '***parameters:'

        for param in params:
            # Name
            if 'name' in param and param['name']:
                parameters_yaml += '\n***  - name: ' + param['name']
            # Origin
            parameters_yaml += '\n***    in: path '
            # Description
            if 'doc' in param and param['doc']:
                parameters_yaml += '\n***    description: ' + \
                    param['doc']
            # Required?
            parameters_yaml += '\n***    required: true'
            # Type
            if 'type' in param and param['type']:
                parameters_yaml += '\n***    type: ' + param['type']
            # Example
            if 'example' in param and param['example']:
                parameters_yaml += '\n***    default: ' + \
                    param['example']

        yaml += '\n' + parameters_yaml

    if is_returns_enabled:
        returns = docstring_dict['returns']
        responses_yaml = '***responses:\n***  200:'

        if 'doc' in returns and returns['doc']:
            responses_yaml += '\n***    description: ' + returns['doc']

        if 'example' in returns and returns['example']:
            responses_yaml += '\n***    example: ' + returns['example']

        if 'type' in returns and returns['type']:
            responses_yaml += '\n***    type: ' + returns['type']

        yaml += "\n" + responses_yaml
    yaml += "\n"

    return add_tabs_to_yaml(yaml, tab_size)
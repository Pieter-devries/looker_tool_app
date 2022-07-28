import re
from flask import flash

operator = "(if|elsif|else|endif)"
value = "{{(.+?)\s}}"
boolean = "{%\s*(.+?)%}"
parameters = "(.+?):\s"
action_variables = [
    "value",
    "rendered_value",
    "filterable_value"
]
default_value_variables = [
    "_user_attributes['name_of_attribute']",
    "_localization['localization_key']"
]
description_variables = [
    "_filters['view_name.field_name']",
    "{% parameter parameter_name %}",
    "parameter_name._parameter_value",
    "_user_attributes['name_of_attribute']",
    "_model._name",
    "_view._name",
    "_explore._name",
    "_field._name",
    "_query._query_timezone",
    "view_name._in_query",
    "view_name.field_name._in_query",
    "view_name.field_name._is_selected",
    "view_name.field_name._is_filtered"
                        ]
filters_variables = [
    "_user_attributes['name_of_attribute']",
    "_localization['localization_key']"
]
html_variables = [
    "value",
    "rendered_value",
    "filterable_value",
    "link",
    "linked_value",
    "_filters['view_name.field_name']",
    "parameter_name._parameter_value",
    "_user_attributes['name_of_attribute']",
    "_model._name",
    "_view._name",
    "_explore._name",
    "_explore._dashboard_url",
    "_field._name",
    "_query._query_timezone",
]
label_variables = [
    "_filters['view_name.field_name']",
    "{% parameter parameter_name %}",
    "parameter_name._parameter_value",
    "_user_attributes['name_of_attribute']",
    "model._name",
    "_view._name",
    "_explore._name",
    "_field._name",
    "_query._query_timezone",
    "view_name._in_query",
    "view_name.field_name._in_query",
    "view_name.field_name._is_selected",
    "view_name.field_name._is_filtered"
]
link_variables = [
    "value",
    "rendered_value",
    "filterable_value",
    "link",
    "linked_value",
    "_filters['view_name.field_name']",
    "parameter_name._parameter_value",
    "_user_attributes['name_of_attribute']",
    "model._name",
    "_view._name",
    "_explore._name",
    "_explore._dashboard_url",
    "_field._name",
    "_query._query_timezone",
    "view_name._in_query",
    "view_name.field_name._in_query",
    "view_name.field_name._is_selected",
    "view_name.field_name._is_filtered"
]
sql_variables = [
    "{% date_start date_filter_name %}",
    "{% date_end date_filter_name %}",
    "{% condition filter_name %}",
    "{% endcondition %}",
    "{% parameter parameter_name %}",
    "parameter_name._parameter_value",
    "_user_attributes['name_of_attribute']",
    "_model._name",
    "_view._name",
    "_explore._name",
    "_field._name",
    "_query._query_timezone",
    "view_name._in_query",
    "view_name.field_name._in_query",
    "view_name.field_name._is_selected",
    "view_name.field_name._is_filtered"
]

def parse(raw_liquid):
    print(re.findall(parameters, raw_liquid))
    parse_dict = parse_booleans(raw_liquid)
    if parse_operators(raw_liquid):
        parse_dict['Operator Check'] = parse_operators(raw_liquid)
    parse_dict.update(parse_values(raw_liquid))

    return parse_dict

def parse_values(raw_liquid):
    parse_dict = dict()
    values = re.findall(f'{value}', raw_liquid)
    fields = list()
    for v in values:
        parsed = re.sub(f'{operator}', '', v)
        if parsed:
            fields.append(parsed)
    value_dict = dict()
    for field in fields:
        parts = field.strip().split('.')
        if len(parts) == 3:
            view_name = parts[0]
            field_name = parts[1]
            variable_name = parts[2]
            value_dict['view_name'] = view_name
            value_dict['field_name'] = field_name
            value_dict['variable_name'] = variable_name
            parse_dict[field] = "Formatting seems correct."
        elif len(parts) == 2:
            field_name = parts[0]
            variable_name = parts[1]
            value_dict['field_name'] = field_name
            value_dict['variable_name'] = variable_name
            parse_dict[field] = "Use view_name.field_name._variable_name format."
        elif len(parts) == 1:
            if parts[0] == "value" or parts[0] == "rendered_value" or parts[0] == "linked_value":
                parse_dict[field] = "Seems fine."
            else:
                parse_dict[field] = "Use view_name.field_name._variable_name format."
        else:
            parse_dict[field] = "Use view_name.field_name._variable_name format."
    return parse_dict

def parse_booleans(raw_liquid):
    parse_dict = dict()
    booleans = re.findall(f'{boolean}', raw_liquid)
    operators = re.findall(f'{operator}', raw_liquid)
    fields = list()
    for b in booleans:
        # parsed = re.sub(f'{operator}', '', b)
        search = re.search(r'^\w+ (\w+)', b)
        if search:
            # print(search.group(1))
            fields.append(search.group(1))
        # if parsed:
        #     fields.append(parsed)
    boolean_dict = dict()
    for field in fields:
        parts = field.strip().split('.')
        if len(parts) == 3:
            view_name = parts[0]
            field_name = parts[1]
            variable_name = parts[2]
            boolean_dict['view_name'] = view_name
            boolean_dict['field_name'] = field_name
            boolean_dict['variable_name'] = variable_name
            parse_dict[field] = "Formatting seems correct."
        elif len(parts) == 2:
            field_name = parts[0]
            variable_name = parts[1]
            boolean_dict['field_name'] = field_name
            boolean_dict['variable_name'] = variable_name
            parse_dict[field] = "Use view_name.field_name._variable_name format."
        elif len(parts) == 1:
            if parts[0] == "value" or parts[0] == "rendered_value" or parts[0] == "linked_value":
                parse_dict[field] = "Seems fine."
            else:
                parse_dict[field] = "Use view_name.field_name._variable_name format."
        else:
            parse_dict[field] = "Too many fields, just use view_name.field_name._variable_name format.\n"
    for b in booleans:
        if not any(o in b for o in operators):
            parse_dict[b] += " Missing operator (If/elsif/endif etc.)"
    return parse_dict

def parse_operators(raw_liquid):
    operators = re.findall(f'{operator}', raw_liquid)
    if len(operators) > 0:
        if_count = operators.count('if')
        endif_count = operators.count('endif')
        if if_count != endif_count:
            if if_count > endif_count:
                return "Not enough endifs."
            else:
                return "Not enough ifs."
        return "Operators seem fine."
    else:
        pass
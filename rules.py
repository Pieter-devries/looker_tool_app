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

field_type_pattern = "(dimension|measure|filters|parameter)"
field_statement_pattern = ":( \w+ {.*?) }[^}]"
parameter_pattern = "(\w+?):\s+"
parameter_statement_pattern = "(.+?)(?: +\w+:| +;;|\Z)"
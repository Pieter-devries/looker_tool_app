import re

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
    "date_start date_filter_name",
    "date_end date_filter_name",
    "condition filter_name",
    "endcondition",
    "parameter parameter_name",
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
field_type_pattern = "(dimension|measure|filters|parameter):"
field_statement_pattern = "( \S+ { .*?) }[ |$]"
parameter_pattern = "(\w+?):"
parameter_statement_pattern = "(.+?)(?= \w+:| ;;)"
liquid_variables = [
            'action',
            'default_value',
            'description',
            'filters',
            'html',
            'label',
            'link',
            'sql'
        ]

field_names = []
field_num = 1
response_dicts = list()

class Fields:
    def __init__(self, raw_liquid):
        # Initialize by importing raw liquid as a single string and removing line breaks
        self.raw_liquid = " ".join(raw_liquid.split())+" "
        self.field_type()

    def field_type(self):
        # Break individual fields apart
        liquid = self.raw_liquid
        # print(liquid)
        fields = re.findall(f'{field_type_pattern}{field_statement_pattern}', liquid)
        for field in fields:
            (_type, _statement) = field
            self.field_statement(_type, _statement)

    def field_statement(self, _type, statement):
        # Itemize different sections of the field statements into a dictionary
        field_dict = dict()
        field_dict['field_type'] = _type
        field_dict['name'] = statement.split(' ')[1]
        parameters = re.findall(f'{parameter_pattern}{parameter_statement_pattern}', statement)
        # print(parameters)
        for (k, v) in parameters:
            field_dict[k] = v
        globals()[field_dict['name']+"_dict"] = field_dict
        field_names.append(field_dict['name'])
        # print(field_dict)
        # Parser(field_dict)

class Parser:
    def __init__(self, field_dict):
        # Using the Fields class to create a dictionary, variablize the separate parts
        self.field_type = field_dict['field_type']
        self.type = field_dict.get('type', 'string')
        self.name = field_dict.get('name')
        self.field_dict = field_dict
        self.perform_magic()


    def perform_magic(self):
        message = dict()
        global field_num
        dict_list = list()
        for lv in liquid_variables:
            if lv in self.field_dict.keys():
                globals()[f'{lv}_dict'] = self.locate_liquid(self.field_dict.get(lv, None), lv)
                # if globals()[f'{lv}_dict']:
                #     print(globals()[f'{lv}_dict'])
                if globals()[f'{lv}_dict']:
                    globals()[f'{field_num}{lv}'] = self.apply_rules(globals()[f'{lv}_dict'], lv)
                    dict_list.append(globals()[f'{field_num}{lv}'])
                    message['name'] = self.name
                    message['header'] = f'For {self.field_type}: {self.name}<br>'
                    message['message'] = self.show_rules(globals()[f'{field_num}{lv}'])
        return message
    def apply_rules(self, liquid_dict, lv):
        # Check if used liquid variable can be used in that parameter
        if liquid_dict.get('mistake_list'):
            liquid_dict['other_mistakes'] = liquid_dict.get('mistake_list')
        if not liquid_dict['check_variable'] in globals()[lv + '_variables']:
            liquid_dict['invalid_variable'] = liquid_dict['full_variable']
        if liquid_dict.get('tag_start') and not liquid_dict.get('tag_end'):
            liquid_dict['missing_tag_end'] = "Missing end for " + liquid_dict.get('tag_start')
        elif liquid_dict.get('tag_end') and not liquid_dict.get('tag_start'):
            liquid_dict['missing_tag_start'] = "Missing start for " + liquid_dict.get('tag_end')
        return liquid_dict

    def show_rules(self, final_dict):
        message = ""
        if final_dict.get('invalid_variable'):
            message += final_dict['invalid_variable'] + "<br>"
        else:
            message += "No issue with variables" + "<br>"
        if final_dict.get('tag_start') or final_dict.get('tag_end'):
            if final_dict.get('missing_tag_start'):
                message += final_dict['missing_tag_start'] + "<br>"
            else:
                message += "No issue with tag_starts" + "<br>"
            if final_dict.get('missing_tag_end'):
                message += final_dict['missing_tag_end'] + "<br>"
            else:
                message += "No issue with tag_ends" + "<br>"
        if final_dict.get('other_mistakes'):
            for row in final_dict.get('other_mistakes'):
                message += row + " is misspelled or missing a tag <br>"
        message = message.rstrip('<br>')
        return message

    def locate_liquid(self, liquid, type):
        # Put the different parts of the field in a liquid checker to locate the liquid
        if not liquid:
            return
        liquid_type = self.statement_type(liquid)
        if liquid_type == "tag":
            tag_dict = self.tag_statement(liquid)
            tag_dict['variable_type'] = type
            return tag_dict
        elif liquid_type == "object":
            obj_dict = self.object_statement(liquid)
            obj_dict['variable_type'] = type
            return obj_dict
        elif liquid_type == "tag, object":
            tag_dict = self.tag_statement(liquid)
            obj_dict = self.object_statement(liquid)
            tag_dict['variable_type'] = type
            obj_dict['variable_type'] = type
            tag_dict.update(obj_dict)
            return tag_dict

    def statement_type(self, statement):
        # print(statement)
        # Identify if liquid exists and split into tag or object
        tag_pattern = "{%\s*(.+?)%}"
        object_pattern = "{{(.+?)\s}}"
        if re.findall(f'{tag_pattern}', statement):
            if re.findall(f'{object_pattern}', statement):
                return "tag, object"
            return "tag"
        elif re.findall(f'{object_pattern}', statement):
            return "object"

    def tag_statement(self, liquid):
        # print(liquid)
        # Break apart individual liquid parts and dictionary them for tags
        tag_pattern = "{%\s*(.+?)%}"
        op_pattern = "(if|elsif|else|endif|parameter|date_start|date_end|condition|endcondition)"
        parse_dict = dict()
        fields = list()
        mistake_list = list()
        operators = re.findall(f'{op_pattern}', liquid)
        for op in operators:
            if op == 'if' or op == 'for' or op == 'date_start' or op == 'condition':
                parse_dict['tag_start'] = op
            elif op == 'else' or op == 'elif':
                parse_dict['tag_mid'] = op
            elif op == 'endif' or op == 'endfor' or op == 'date_end' or op == 'endcondition':
                parse_dict['tag_end'] = op
            elif op == 'parameter':
                parse_dict['parameter'] = 'parameter'
        # print(operators)
        tag_statement = re.findall(f'{tag_pattern}', liquid)
        # print(tag_statement)
        for t in tag_statement:
            search = re.search(f'{op_pattern} +(\S+)', t)
            if search:
                fields.append(search.group(2))
        # print(fields)
        for field in fields:
            parts = field.strip().split('.')
            # print(parts)
            if parse_dict.get('parameter'):
                parse_dict['field_name'] = parts[0]
                parse_dict['full_variable'] = parse_dict['parameter'] + " " + parts[0]
                parse_dict['check_variable'] = parse_dict['parameter'] + " parameter_name"
            else:
                if len(parts) == 3:
                    parse_dict['view_name'] = parts[0]
                    parse_dict['field_name'] = parts[1]
                    parse_dict['variable_name'] = parts[2]
                    parse_dict['full_variable'] = f'{parts[0]}.{parts[1]}.{parts[2]}'
                    parse_dict['check_variable'] = f'view_name.field_name.{parts[2]}'
                elif len(parts) == 2:
                    parse_dict['field_name'] = parts[0]
                    parse_dict['variable_name'] = parts[1]
                    parse_dict['full_variable'] = f'{parts[0]}.{parts[1]}'
                    parse_dict['check_variable'] = f'field_name.{parts[1]}'
                elif len(parts) == 1:
                    if parts[0] == "value" or parts[0] == "rendered_value" or parts[0] == "linked_value":
                        parse_dict['variable_name'] = parts[0]
                        parse_dict['full_variable'] = f'{parts[0]}'
                        parse_dict['check_variable'] = f'{parts[0]}'
                    else:
                        parse_dict['message'] = "Variable missing."
                else:
                    parse_dict['message'] = "Too many fields."
        for mistakes in tag_statement:
            if not any(o in mistakes for o in operators):
                parse_dict[mistakes] = "Missing operator (If/elsif/endif etc.) or misspelled."
                mistake_list.append(mistakes)
        parse_dict['mistake_list'] = mistake_list
        return parse_dict

    def object_statement(self, liquid):
        # Break apart individual liquid parts and dictionary them for objects
        value_pattern = "{{(.+?)\s}}"
        parse_dict = dict()
        obj_statement = re.findall(f'{value_pattern}', liquid)
        for idx, each in enumerate(obj_statement):
            parse_dict[f'obj_{idx}'] = each
        return parse_dict


liquid_input = """
dimension: id {
  primary_key: true
  type: number
  sql: ${TABLE}.id ;;
  html:
    {% if value > 10 %}
      <font color="darkgreen">{{ rendered_value }}</font>
    {% elsif value > 11 %}
      <font color="goldenrod">{{ rendered_value }}</font>
    {% else %}
      <font color="darkred">{{ rendered_value }}</font>
    {% endif %} ;;
}

measure: value {
  sql:
      {% if users_sql_based_dt.city._is_filtered %}
      ${TABLE}.status
      {% endif %} ;;
  type: string
}
  measure: dynamic_measure {
    description: "Use with Metric_Picker Filter Only"
    type: number
    label_from_parameter: metric_chooser
    sql:    CASE
      WHEN {% date_start metric_chooser %} = 'views'
        THEN ${views}
      WHEN {% parameter metric_chooser %} = 'avg_watch_time'
        THEN ${avg_watch_time}
      WHEN {% parameter metric_chooser %} = 'subscriber_change'
        THEN ${subscriber_change}
        WHEN {% parameter metric_chooser %} = 'shares'
        THEN ${shares}
        WHEN {% parameter metric_chooser %} = 'like_change'
        THEN ${like_change}
        WHEN {% parameter metric_chooser %} = 'key_points'
        THEN ${key_points}
      ELSE NULL
    END ;;
  } 
  
"""
#
#
# def create_field_dict(liquid_input):
#     Fields(liquid_input)
#
#
# def parse_fields(field_dict):
#     message = Parser(field_dict)

def main(liquid_input):
    Fields(liquid_input)
    for field in field_names:
        parse_object = Parser(globals()[field+"_dict"])
        globals()["parsed_" + field + "_dict"] = parse_object.perform_magic()
        response_dicts.append(globals()["parsed_" + field + "_dict"])
    return response_dicts

if __name__ == "__main__":
    Fields(liquid_input)
    for field in field_names:
        parse_object = Parser(globals()[field+"_dict"])
        globals()["parsed_" + field + "_dict"] = parse_object.perform_magic()
        response_dicts.append(globals()["parsed_" + field + "_dict"])
    print(response_dicts)




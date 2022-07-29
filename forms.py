from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

default_value = """### DEFAULT INPUT FOR TESTING, DELETE IF YOU LIKE ###
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
        WHEN {% metric_chooser %} = 'shares'
        THEN ${shares}
        WHEN {% parmeter metric_chooser %} = 'like_change'
        THEN ${like_change}
        WHEN {% parametr metric_chooser %} = 'key_points'
        THEN ${key_points}
      ELSE NULL
    END ;;
  } """

class LiquidLinter(FlaskForm):
    liquid_text = TextAreaField('Liquid Text', validators=[DataRequired()], default=default_value)
    submit = SubmitField('Validate')

class DeleteMessage(FlaskForm):
    delete = SubmitField('Delete')


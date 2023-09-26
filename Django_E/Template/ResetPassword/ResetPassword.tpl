{% extends "mail_templated/base.tpl" %}

{% block subject %}
    Reset Password
{% endblock %}

{% block body %}
    http://127.0.0.1:8000/account/api/v1/reset_password_check_token/{{token}}
{% endblock %}
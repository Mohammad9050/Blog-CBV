{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello 
{% endblock %}

{% block body %}
http://127.0.0.1:8000/accounts/api/v1/activation-code/{{token}}
{% endblock %}

{% block html %}

{% endblock %}
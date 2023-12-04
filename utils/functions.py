
import json
import decimal

from django.db import models
from django.db import connection
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# customer sql query
def customer_sql(sql):
    c = connection.cursor()
    try:
        c.execute(sql)
        row = dictfetchall(c)
        c.close()
        return row
    except TypeError:
        c.close()
        return None

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        from datetime import datetime, date
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, models.Model):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """
    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator

# url view check  permission
def check_permisson(permisson, view):
	return login_required( permission_required(permisson, raise_exception=True)(view) )


# template view
def templateView(html):
	return TemplateView.as_view(template_name=html)


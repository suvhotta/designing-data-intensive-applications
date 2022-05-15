## QuerySet and Manager:
- Queryset can be thought of as a SELECT statement in django. they can be chained  with
    various filters.
- Manager is an abstraction layer that provides us the queryset. Each model has at-least one Manager and its called
    objects by default. It can be accessed from the Class and not from the instance.
    `Blog.objects`
    Manager is the main source of QuerySets for a model. Eg: Blog.objects.all() returns a QuerySet that contains all
    Blog objects in the DB.
- We can always change the default manager to a model, if required. The manager's get_queryset() method returns the 
    query results. In case we need some kind of filtering like the user is active or not, we can put a check directly
    in the get_queryset method instead of manually adding everytime while querying.
- We can also attach multiple managers to a model and use them as and when needed during querying.
- We also create an instance of Manager with a copy of a custom QuerySet's methods like: `PersonQuerySet.as_manager()`


## Tables
- By default, app name will be appended as prefix to the table created. To bypass this behaviour, add the db_table name
    to the Meta class of the model.
    https://docs.djangoproject.com/en/4.0/ref/models/options/

## Read-only, Write-only params:
- For additional serializer fields which aren't part of the model, the read-only and write-only params
    need to pass during the field creation.
    Eg: `clinician_id = serializers.UUIDField(format='hex_verbose', write_only=True)`
    If the same is being passed on in the class Meta, it won't be accepted and hence the property won't be reflected.
- For the read-only/write-only restrictions on model fields, it needs to be explicitly mentioned in the class Meta of the 
    serializer.


## Django Signals:
- Once added listeners for the signals in a separate singals file, it needs to be added to the app.py file of corresponding app.
- If using signals, then the app's config file needs to be registered in the settings file, instead of the app only.
    Instead of simply <app_name> it will now be <app_name>.apps.<app_name>Config
    OR if we don't wish to add the config file directly to the settings, then we could add the following to the init.py file 
    of the app `default_app_config='<app_name>.apps.<app_name>Config'` and continue registering only the <app_name>
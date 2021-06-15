## Refactoring if-else statements to a OOP model

 

#### The problem

 

Let's look at this horrible piece of code and try to refactor it to the point of understanding:

 

```

data['code_replaced'] = copy.deepcopy(data['code'])

    for parameter, values in data['extraction_parameters'].items():

        if values['parameter_type'] == 'double' and values['label_of_data']:

            if values['label_of_data'] in config.labels:

                suggestion = config.labels[values['label_of_data']].get_last_reference()

                values['suggested_value'] = suggestion['reference']

                values['suggested_date'] = suggestion['date']

                data['code_replaced'] = data['code_replaced'].replace('@{}:N'.format(parameter),

                                                                      str(suggestion['reference']))

            else:

                values['suggested_value'] = None

                values['suggested_date'] = None

        elif values['parameter_type'] == 'double':

            if values['value']:

                data['code_replaced'] = data['code_replaced'].replace('@{}:N'.format(parameter),

                                                                      str(values['value']))

        elif values['parameter_type'] == 'string':

            if not values['chooser_value'] and values['value']:

                if 'MxSQLExpression' in values['name']:

                    data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(parameter),

                                                                          str(values['value']))

                else:

                    data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(parameter),

                                                                          "'{}'".format(values['value'].strip("'")))

            elif values['chooser_value']:

                data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(parameter), " in ({})".format(

                    str(values['chooser_value'].decode('ISO-8859-1'))))

        elif values['parameter_type'] == 'other':

            if values['value']:

                data['code_replaced'] = data['code_replaced'].replace('@{}:S'.format(parameter),

                                                                      "'{}'".format(

                                                                          str(values['value']).strip("'")))

```

 

Here's the main question: "what is the second line: ```for parameter, values in data['extraction_parameters'].items():```?"

 

The name is confusing, because "parameter" for me means "variable" and "values" mean "groups of variables" so they don't mean anything. I would propose to change them to ```for param_name, param_obj in data['extraction_parameters'].items():```. In this way we can see a relation between the name and the object in a dictionary ```data['extraction_parameters']```.

 

```param_obj``` is also in fact a dictionary. It is not a bad idea to use dictionaries if you don't see a polymorphic pattern or the keys in that dictionary are not standarized. What do I mean by this?

 

1. If you need to store variable amount of keys in a dictionary, then use a dictionary

2. If you use a static list of keys in a dictionary, then you probably have a new class there.

 

*"But what if I have a static list of 6 keys but I use 3 keys in one if-statement and other 3 in another if-statement"* - then you have no idea what you are doing:) This is a classic polymorphic issue and probably you should have:

1. 2 different classes which share an abstraction with only 3 attributes.

2. 2 classes which do not share an abstraction with each having it's own set of attributes.

 

**If you didn't understand the statement above, then I hope the example below will explain everything.**

 

 

#### Moving from dictionaries to objects

 

Let's refactor the code so that all ```param_obj['any_key']``` will translate to an attribute like ```param_obj.any_key```:

 

```

data['code_replaced'] = copy.deepcopy(data['code'])

    for param_name, param_obj in data['extraction_parameters'].items():

        if param_obj.parameter_type == 'double' and param_obj.label_of_data:

            if param_obj.label_of_data in config.labels:

                suggestion = config.labels[param_obj.label_of_data].get_last_reference()

                param_obj.suggested_value = suggestion['reference']

                param_obj.suggested_date = suggestion['date']

                data['code_replaced'] = data['code_replaced'].replace('@{}:N'.format(param_name),

                                                                      str(suggestion['reference']))

            else:

                param_obj.suggested_value = None

                param_obj.suggested_date = None

        elif param_obj.parameter_type == 'double':

            if param_obj.value:

                data['code_replaced'] = data['code_replaced'].replace('@{}:N'.format(param_name),

                                                                      str(param_obj.value))

        elif param_obj.parameter_type == 'string':

            if not param_obj.chooser_value and param_obj.value:

                if 'MxSQLExpression' in param_obj.name:

                    data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(param_obj),

                                                                          str(param_obj.value))

                else:

                    data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(param_name),

                                                                          "'{}'".format(param_obj.value.strip("'")))

            elif param_obj.chooser_value:

                data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(param_obj), " in ({})".format(

                    str(param_obj.chooser_value.decode('ISO-8859-1'))))

        elif param_obj.parameter_type == 'other':

            if param_obj.value:

                data['code_replaced'] = data['code_replaced'].replace('@{}:S'.format(param_name),

                                                                      "'{}'".format(

                                                                          str(param_obj.value).strip("'")))

```

 

#### Finding new classes

 

Now let's understand what the first level of if-else statements refers to:

 

```

...

if param_obj.parameter_type == 'double' and param_obj.label_of_data:

    ...

elif param_obj.parameter_type == 'double':

    ...

elif param_obj.parameter_type == 'string':

    ...

elif param_obj.parameter_type == 'other':

    ...

```

 

This is a hard indication that we have classes like "double", "string" and "other" which may or may not share the same abstraction / API.

 

 

#### Finding attributes

 

Let's see what is in the first and second level of if-else statements:

```

if param_obj.parameter_type == 'double' and param_obj.label_of_data:

    if param_obj.label_of_data in config.labels:

        ...

    else:

        ...

elif param_obj.parameter_type == 'double':

    if param_obj.value:

        ...

elif param_obj.parameter_type == 'string':

    if not param_obj.chooser_value and param_obj.value:

        if 'MxSQLExpression' in param_obj.name:

            ...

        else:

            ...

    elif param_obj.chooser_value:

        ...

elif param_obj.parameter_type == 'other':

    if param_obj.value:

        ...

```

 

Look at this pattern:

- When parameter_type is "double" and object has "label_of_data" attribute, then use "label_of_data"

- When parameter_type is "double" and object does not have "label_of_data" attribute, then use "value"

- When parameter_type is "string" use "chooser_value"

- When parameter_type is  "other" use "value".

 

So it looks like the following attributes "label_of_data", "value", "chooser_value" are just attribute "value" which are specific for each different class.

 

#### Cascading statements

 

For the below line of code we can see that we **cannot** swap ```if``` with ```elif``` e.g.

 

from this:

 

```

if values['parameter_type'] == 'double' and values['label_of_data']:

    ...

elif values['parameter_type'] == 'double':

```

to this:

 

```

if values['parameter_type'] == 'double':

    ...

elif values['parameter_type'] == 'double' and values['label_of_data']:

```

 

This will give a different result and will be an issue when refactoring in an OOP way. The easiest way to fix it beforehand is to fill out the implicite statement:

 

```

if values['parameter_type'] == 'double' and not values['label_of_data']:

    ...

elif values['parameter_type'] == 'double' and values['label_of_data']:

 

```

 

 

#### Defining common action - finding methods

 

We need to understand the mutual action each if-else statement makes. Let's cut it out:

 

```

...

data['code_replaced'] = data['code_replaced'].replace('@{}:N'.format(param_name),

...

data['code_replaced'] = data['code_replaced'].replace('@{}:N'.format(param_name),

                                                                     str(param_obj.value))

...

data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(param_obj),

                                                                     str(param_obj.value))

...

data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(param_name),

                                                      "'{}'".format(param_obj.value.strip("'")))

...

data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(param_obj), " in ({})".format(

    str(param_obj.chooser_value.decode('ISO-8859-1'))))

...

data['code_replaced'] = data['code_replaced'].replace('@{}:S'.format(param_name),

                                                      "'{}'".format(

                                                          str(param_obj.value).strip("'")))

...

```

 

The action is to replace a string in a string of some code. In this case it replaces a Murex-specific @MxDataSetKey:N (or similar) parameter with a value in a SQL query. In the old version of the code we have the impression that the most pressing matter is the "replace" method but that is not true. **The biggest issue is which value should we use**

 

**Using a massive if-else statement will burry the true algorithm of your code. Any further refactoring/enhancing will be a problem for newcomers to the code-base as well as for the same developer who wrote it.**

 

 

side note: We can also see errors in the code:

 

```

# param_obj used

data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(param_obj),

                                                                     str(param_obj.value))

 

# param_name used

data['code_replaced'] = data['code_replaced'].replace('@{}:C'.format(param_name),

                                                      "'{}'".format(param_obj.value.strip("'")))

```

 

```param_obj``` was previously a dictionary. Evaluated to a string would look like ```"{'key1': 'value1', ...}"```. This string would never exist in a SQL query so this replacement would never be executed. So there are lines of code that were never correct and nobody so the difference. Secondly do we know that ```param_name``` is the correct value, not ```param_obj.name```?

 

### OOP Refactoring

 

The goal is to get the following solution:

 

```   

data['code_replaced'] = copy.deepcopy(data['code'])

for param_name, param_obj in data['extraction_parameters'].items():

    data['code_replaced'] = param_obj.replace_in_sql_query(data['code_replaced'])

```

 

Let's have a abstract class and children

 

```

import abc

from reptool.backend import ConfigsDict  # singleton

 

 

class AbstractParameter(abc.ABC):

    def __init__(self, name, value: str):

        self.name = name

        self.value = value

 

    @property

    @abc.abstractmethod

    def replace_template(self) -> str:

        ...

 

 

    @abc.abstractmethod

    def replace_in_sql_query(self, sql_query: str) -> str:

        ...

 

 

class DoubleParameter(AbstractParameter):

    replace_template =  "@{}:N"

    def __init__(self, name, value, label_of_data=None):

        super().__init__(name, value)

        self.label_of_data = label_of_data

 

    def replace_in_sql_query(self, sql_query: str) -> str:

        config = ConfigsDict()[murex][environment]

        if self.label_of_data in config.labels:

            suggestion = config.labels[self.label_of_data].get_last_reference()

            self.suggested_value = suggestion["reference"]

            self.suggested_date = suggestion["date"]

            replaced_str = sql_query.replace(

               replace_template.format(self.name), str(suggestion["reference"])

            )

        else:

            replaced_str = sql_query.replace(replace_template.format(self.name), str(self.value))

 

        return replaced_str

 

 

class StringParameter(AbstractParameter):

    replace_template = "@{}:C"

    def __init__(self, name, value: str, chooser_value=None):

        super().__init__(name, value)

        self.chooser_value = chooser_value

 

    def replace_in_sql_query(self, sql_query: str) -> str:

        replaced_str = sql_query

        if not self.chooser_value and self.value:

            if "MxSQLExpression" in self.name:

                replaced_str = sql_query.replace(replace_template.format(self), self.value)

            else:

                replaced_str = sql_query.replace(

                    replace_template.format(self.name), "'{}'".format(self.value.strip("'"))

                )

        elif self.chooser_value:

            replaced_str = sql_query.replace(

                replace_template.format(self.name),

                " in ({})".format(str(self.chooser_value.decode("ISO-8859-1"))),

            )

 

        return replaced_str

 

 

class OtherParameters(AbstractParameter):

    replace_template = "@{}:S"

    def replace_in_sql_query(self, sql_query: str) -> str:

        replaced_str = sql_query.replace(

           replace_template.format(self.name), "'{}'".format(str(self.value).strip("'"))

        )

        return replaced_str

 

 

 

```

 

#### Unification of attributes

 

1. The method ```replace_in_sql_query``` **cannot** implicitly modify the internal structure of the class especially when doing something else. Assigning an internal value which is not part of the replace method ```self.suggested_value = suggestion["reference"]``` is that precise error.

2. We need to unify all attributes. We cannot have different ```__init__``` signature between inheriting classes.

3. Try to make ```replace_in_sql_query``` as generic as possible and hopefully move it to the AbstractParameter class.

3. Remove and group all beautifying functionalities like ```str(value).strip("'")```. Data should be correct beforehand or a new method/property should be created to provide a beautifying funcionality.

 

Lets work on each class:

 

```

class DoubleParameter(AbstractParameter):

    replace_template = "@{}:N"

 

    def __init__(self, name, value):

        config = ConfigsDict()[murex][environment]

        try:

            suggestion = config.labels[self.label_of_data].get_last_reference()

            super().__init__(name, suggestion["reference"])

        except KeyError:

            super().__init__(name, value)

 

    def replace_in_sql_query(self, sql_query: str) -> str:

        replaced_str = sql_query.replace(replace_template.format(self.name), str(self.value))

        return replaced_str

```

 

But usage of a singleton within this class is incorrect, because the class should not encapsulate context which is outside of this class. So we would move the ```config = ConfigsDict()``` outside to a factory pattern which we will discuss in a different snippet. So:

 

```

class DoubleParameter(AbstractParameter):

    replace_template = "@{}:N"

 

 

    def replace_in_sql_query(self, sql_query: str) -> str:

        replaced_str = sql_query.replace(self.replace_template.format(self.name), self.value)

        return replaced_str

       

 

def get_parameter(name, value):  # part of a factory pattern implementation

    config = ConfigsDict()[murex][environment]

    try:

        suggestion = config.labels[self.label_of_data].get_last_reference()

        obj = DoubleParameter(name, suggestion["reference"])

    except KeyError:

        obj = DoubleParameter(name, value)

    

    return obj

```

 

Let's go with the next class:

 

```

class StringParameter(AbstractParameter):

    replace_template = "@{}:C"

 

    def __init__(self, name, value: str):

        value = value.strip("'") if "MxSQLExpression" not in name else value

        super().__init__(name, value)

 

    def replace_in_sql_query(self, sql_query: str) -> str:

        replaced_str = sql_query.replace(self.replace_template.format(self.name), self.value)

        return replaced_str

 

 

def get_parameter(name, value):  # part of a factory pattern implementation

    try:

        value = value.decode("ISO-8859-1")

    except AttributeError:

        pass

    obj = StringParameter(name, value)

    return obj

```

 

#### Remove beautification

 

```

class OtherParameter(AbstractParameter):

    replace_template = "@{}:S"

 

    def __init__(self, name, value):

        super().__init__(name, str(value).strip("'"))

 

    def replace_in_sql_query(self, sql_query: str) -> str:

        replaced_str = sql_query.replace(

            self.replace_template.format(self.name), "'{}'".format(self.value)

        )

        return replaced_str

```

 

We're stripping the value from single quotes ```str(value).strip("'")``` and then adding single quotes ```"'{}'".format(self.value)``` in far too many places. Let's remove that discrepency and let tests figure out if there really is a "single quote issue" here. Additionally let's add a property raw_value were we will give the possibility of removing quotes if they exist.

 

```

class OtherParameter(AbstractParameter):

    replace_template = "@{}:S"

 

    @property

    def raw_value(self):

        return self.value.strip("'")

 

    def replace_in_sql_query(self, sql_query: str) -> str:

        replaced_str = sql_query.replace(self.replace_template.format(self.name), self.value)

        return replaced_str

```

 

We can now see that the ```replace_in_sql_query``` method is exactly the same for all subclasses. The only thing that really differs is the input or the ```replace_template``` attribute.

 

### Final state

 

```

import abc

 

 

class AbstractParameter(abc.ABC):

    def __init__(self, name, value: str):

        self.name = name

        self.value = value

 

    @property

    @abc.abstractmethod

    def replace_template(self) -> str:

        ...

 

    @property

    def raw_value(self):

        return self.value.strip("'")

 

    def replace_in_sql_query(self, sql_query: str) -> str:

        replaced_str = sql_query.replace(self.replace_template.format(self.name), self.value)

        return replaced_str

 

 

class DoubleParameter(AbstractParameter):

    replace_template = "@{}:N"

 

 

class OtherParameter(AbstractParameter):

    replace_template = "@{}:S"

 

 

class StringParameter(AbstractParameter):

    replace_template = "@{}:C"

 

 

def get_StringParameter(name, value):  # part of a factory pattern implementation

    try:

        value = value.decode("ISO-8859-1")

    except AttributeError:

        pass

    obj = StringParameter(name, value)

    return obj

 

 

def get_DoubleParameter(name, value, config):  # part of a factory pattern implementation

    try:

        suggestion = config.labels[value].get_last_reference()

        obj = DoubleParameter(name, suggestion["reference"])

    except KeyError:

        obj = DoubleParameter(name, value)

 

    return obj

 

```

 

Now this will work in a polymorphic fashion:

 

```   

code_copy = copy.deepcopy(data['code'])

for param_obj in data['extraction_parameters'].values():

    code_copy = param_obj.replace_in_sql_query(code_copy)

data['code_replaced'] = code_copy

```

 

 

**Now you just have to instantiate the correct subclass for each parameter, but that will be covered in the next snippet (hopefully in a shorter version).**

 

 

*Created by Kris, Krzysztof.Urbanczyk@unicredit.eu*
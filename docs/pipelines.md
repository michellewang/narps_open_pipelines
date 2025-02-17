# Writing pipelines :writing_hand:

Here are a few principles you should know before creating a pipeline. Further in this file, replace `<team_id>` by the actual team ID (4 letters / digits) the pipeline refers to (e.g.: `2T6S`).

Please apply these principles in the following order.

## Create a file containing the pipeline
The pipeline must be contained in a single file named `narps_open/pipelines/team_<team_id>.py`.

## Inherit from `Pipeline`
In this file, create a `class` named `PipelineTeam<team_id>` that inherits from the `narps_open.pipelines.Pipeline` class. Here is a sample code:
```python
from narps_open.pipelines import Pipeline

class PipelineTeam2T6S(Pipeline):
    """ A class that defines the pipeline of team 2T6S. """
```

## Create the signatures and docstrings for the mandatory methods

The `narps_open.pipelines.Pipeline` class declares abstract methods that must be implemented in your pipeline so that it works. These are:

```python
def get_preprocessing(self):
    """ Return a Nipype workflow describing the prerpocessing part of the pipeline """

def get_run_level_analysis(self):
    """ Return a Nipype workflow describing the run level analysis part of the pipeline """

def get_subject_level_analysis(self):
    """ Return a Nipype workflow describing the subject level analysis part of the pipeline """

def get_group_level_analysis(self):
    """ Return a Nipype workflow describing the group level analysis part of the pipeline """
```

If one of these four steps was not performed by the team, simply make the corresponding method return `None`. Here is an example:

```python
def get_preprocessing(self):
    """ No preprocessing has been done by the team, fMRIprep data was used """
    return None
```

## Actually implement the methods

It is time to dive into the pipeline's logic!
Note that each of the previously declared methods must return a Nipype workflow.
Please find the documentation of Nipype [here](https://nipype.readthedocs.io/en/latest/).
Have a look at this Nipype [tutorial](https://miykael.github.io/nipype_tutorial/) if you are not familiar with the library.

Here is an example of what a workflow architecture should look like:
```python
# Create nodes for the pipeline, each Node takes an interface as a parameter.
# (Here we removed the attributes passed to each interface, for readability reasons)
info_source = Node(IdentityInterface(), name = 'infosource')
select_files = Node(SelectFiles(), name = 'selectfiles')
smoothing = Node(Smooth(), name = 'smooth')
# etc.

# Create workflow
analysis = Workflow(base_dir = self.directories.working_dir, name = 'l1_analysis')

# Connect the nodes inside the workflow
l1_analysis.connect([
    (info_source, select_files, [('param_1', 'param_2')]), # Here we connect param_1 (output of info_source) to param_2 (input of select_file)
    (select_file, smoothing, [('param_3', 'param_4')])
    ])
```

Whenever the interface you need is not available in the Nipype library, you may use the `Function` interface, which is a way to define your custom interface.
See [details here](https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.utility.wrappers.html#function), and [how to use it](https://miykael.github.io/nipype_tutorial/notebooks/basic_function_interface.html).

## Implement the output methods

Also implement the output methods, which list all of the files each step of the pipeline is supposed to generate. Use the following signatures:

```python
def get_preprocessing_outputs(self):
    """ Return the names of the files the preprocessing is supposed to generate. """

def get_run_level_outputs(self):
    """ Return the names of the files the run level analysis is supposed to generate. """

def get_subject_level_outputs(self):
    """ Return the names of the files the subject level analysis is supposed to generate. """

def get_group_level_outputs(self):
    """ Return the names of the files the group level analysis is supposed to generate. """
```

:warning: Do not declare the method if no files are generated by the corresponding step. For example, if no preprocessing was done by the team, the `get_preprocessing_outputs` method must not be implemented.

You should use other pipeline attributes to generate the lists of outputs dynamically. E.g.:

```python
def get_subject_level_outputs(self):
    """ Return the names of the files the subject level analysis generates. """

    # Here we create a list of contrat map templates, using a comprehension list
    # self.directories.output_dir is a pipeline attribute, as well as self.contrast_list
    # subject_id will be filled later using a formatting string
    templates = [join(
        self.directories.output_dir,
        'l1_analysis', '_subject_id_{subject_id}', f'con_{contrast_id}.nii')\
        for contrast_id in self.contrast_list]

    # Here we replace the subject_id by actual values for each subject included in the analysis
    return_list = []
    for template in templates:
        return_list += [template.format(subject_id = s) for s in self.subject_list]

    return return_list
```

## Use attributes from the `Pipeline` class

As explained before, all pipeline inherit from the `narps_open.pipelines.Pipeline` class, hence having access to a set of attributes, such as:
* `directories` : a set of paths the pipeline needs to access such as the input dataset, the output directory, etc.) ;
* `subject_list` : the list of participants on which to run the pipeline ;
* `run_list` : the list of runs to use, e.g.: `['01', '02', '03', '04']` to use all runs ;
* `constrast_list` : the list of contrats computed by the first level analysis and used in the group level analysis ;
* `team_id` : ID of the team (e.g.: `2T6S`) ;
* `fwhm` : full width at half maximum for the smoothing kernel (in mm) :
* `tr` : repetition time of the fMRI acquisition (equals 1.0s)

## Test your pipeline

First have a look at the [testing topic of the documentation](./docs/testing.md). It explains how testing works for inside project and how you should write the tests related to your pipeline.

Feel free to have a look at [tests/pipelines/test_team_2T6S.py](./tests/pipelines/test_team_2T6S.py), which is the file containing all the automatic tests for the 2T6S pipeline : it gives a good example.

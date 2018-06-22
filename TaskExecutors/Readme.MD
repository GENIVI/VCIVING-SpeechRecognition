Contents
===========

TaskExecutors which are called when speech recognition and interpretation has been done.
These TaskExecutors interact with the IVI system.

Requirements
===============

This directory is intended to have a json file called "struct.json", which would contain information about the present
TaskExecutors in the following format.

`
{
    "abstract": {
        "package" : %The name of the folder inside the parent directory which contains all the abstract classes%,
        "namespace": %The filename of the python file which defines TaskExecutor class%,
        "class": %The name of the class of TaskExecutor interface.(This is usually "TaskExecutor")%
    }
    "dependencies_directories" : [
        %Dependency Directory 1%, %Dependency Directory 2%, %Dependency Directory 3%, ...
    ],

    "executors": [
        {
            "namespace" : %Executor Directory Name%,
            "class": %Executor Namespace python file inside the namespace folder%
        },
        {
            ..
        },
        ...
    ]

}
`
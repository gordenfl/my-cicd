# my-cicd

My practice of CI/CD.

1. What is CI/CD
    this is a process of how to publish code to an env automatic and it have several kinds of way to deal that:
    * GitHub Actions
    * Jenkins
    * other ways

    This document we just using GitHub Actions to deal with that. I will give you a full process of public the project of Python Django

2. CI/CD
    * start an github repos at the Github pages, we call it my-cicd
    * Click Action tab in the main page of the repos in Github, we can choose Django to
    * .github/workflow/django.yaml will be appeal in our project
    * read the content of this file, we can see that all the struct has been finished.

3. Content of That Yaml
    basic it will have four parts of that file:
    * name: name of the project
    * on: what actio    n it can be on this project (push, pull_request etc.)
    * jobs: this is the most complicated part of this file, just define different step of the action while will be done on the process
    * jobs/build : here you can define different actions to doing something you want. and it depend on what action name you defined, such as "- uses: actions/checkout@v4", that means you need to execute the logic define in the action's checkout at the ver 4. jobs/build have different other attribute.
    * jobs/build/runs-on: that means that what's the main docker image your project will running on.
    * jobs/build/strategy : define the attribute of the project
    * jobs/build/steps: is defined all the step it will execute while we using CI/CD, this part is most important. each command line will start with "- ". It based on the action and action arguments.
    * jobs/build/run: define the shell command will run in the docker instance

    this is a example of that file :

    ```yaml
    name: Django CI

    on:
        push:
            branches: [ "main" ]
        pull_request:
            branches: [ "main" ]

    jobs:
        build:
            runs-on: ubuntu-latest
            strategy:
                max-parallel: 4
                matrix:
                    python-version: [3.7, 3.8, 3.9]

            steps:
            - uses: actions/checkout@v4
            - name: Set up Python ${{ matrix.python-version }}
            uses: actions/setup-python@v3
            with:
                python-version: ${{ matrix.python-version }}
            - name: Install Dependencies
            run: |
                python -m pip install --upgrade pip
                pip install -r requirements.txt
            - name: Run Tests
            run: |
                python manage.py test

    ```

    if the pull_request defined branches does not include what branch you send pull_request, the error will be happened.

    and you can see the output from 

4. All Actions
    * you can visit the URL: "https://www.github.com/actions" to get all actions pre-defined by the open source world.
    different kinds of action will do different things you can use that yaml to finish what you want. and if you want know what is the main logic of that action, you can read that file there.
    It has the document there, you can read that while you confused

5. How to make Docker Image
    * you can go to the docker hub and 
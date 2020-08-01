## Important Guidelines

1. Write code and commit on your own branch only. (No commits on master branch). Feel free to make as many branches as you like.
2. Do not modify existing code blocks(classes, functions, models, api, views, etc.) to fit your task needs. If you want to reuse a code block, reuse as it is. Or else make your own. Then code optimization and refactoring will be done later at the end of an iteration.
3. Always comment your code blocks such that other devs can understand its purpose. Example:- 1 or 2 line description about a function.
4. Avoid using (Shift+Delete). Recycle Bin is a friend in need, indeed......
5. After pulling, check for any python package updates. If any, run `pipenv install` to install the new packages. Also, run database migrations.
6. Thoroughly test before opening a Pull Request.
7. Any other important guideline for the team should be highlighted here in Readme.md in bold.
8. As a convention, prefix model fields and form fields with model name. 
    Eg:- `class Stud(models.Model):
            stud_name, stud_age.`

## Setting up The Repo 1st Time on Local System

1.  Fork the repo to your account.
2.  Clone the repo on your computer.

3.  Add remote upstream for fetching / pulling from the original project repo.(Fetch/Pull Updates from upstream. And Push your commits to origin)

    `git remote add upstream https://github.com/dhruvparekh12/sih-sikkim.git`

4.  Checkout to Your own branch.

    `git checkout -b br_name`

5.  Setup Environment and dependencies. (Requires python 3.7 and pipenv installed). Enter these commands in the repo root directory.(where Pipfile exist.)

    `pipenv install`

    `pipenv shell`

6.  Setup Database.

    `cd src`

    `python manage.py migrate`

    `python manage.py createsuperuser`

7.  Run Server.

    `python manage.py runserver`

## Additional Notes

- Django Admin Panel can be accessed at:

  `/admin-control-panel/`

- MDBootstrap Documentation

    https://mdbootstrap.com/docs/standard/forms/overview/

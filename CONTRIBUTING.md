# Contributing

The scripts to generate the OPC UA models live in [dev_scripts/](dev_scripts/).

## Dependencies

Before you can run the generation scripts, you have to create a virtual environment to install the dependencies:

```
python -m venv venv
```

... and activate it on Linux/Mac:

```
source venv/bin/activate
```

... or on Windows:

```
venv/Scripts/Activate.bat
```

Finally, you can install the dependencies with `pip`:

```
pip3 install --editable .[dev]
```

## Precommit Checks

To run all pre-commit checks, run from the root directory:

```
python continuous_integration/precommit.py
```

You can automatically re-format the code and fix certain files automatically with:

```
python continuous_integration/precommit.py --overwrite
```

The pre-commit script also runs as part of our continuous integration pipeline.

## Commit Messages

We follow Chris Beams' [guidelines on commit messages]:

1) Separate subject from body with a blank line
2) Limit the subject line to 50 characters
3) Capitalize the subject line
4) Do not end the subject line with a period
5) Use the imperative mood in the subject line, full sentences in the body
6) Wrap the body at 72 characters
7) Use the body to explain *what* and *why* vs. *how*

[guidelines on commit messages]: https://chris.beams.io/posts/git-commit/

If you are merging in a pull request, please squash before merging.
We want to keep the Git history as simple as possible, and the commits during the development are rarely insightful later.

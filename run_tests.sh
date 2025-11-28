#!/bin/bash
# Add the current directory to PYTHONPATH so the 'tests' module can be found
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the Django tests
# We point to the manage.py file and tell it to run the 'tests' directory
python3 fewo_web/fewo/manage.py test tests

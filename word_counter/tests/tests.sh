#! /bin/bash

pip install pytest black isort freezegun
pytest
isort --check app tests
black --check app tests
#!/bin/bash
if [ $1 == "start" ];
then
    poetry run python -m app.main
elif [ $1 == "format" ];
then
    poetry run python -m ruff format app/
    poetry run python -m ruff check --fix app/
    poetry run mypy app/
elif [ $1 == "test" ];
then
    export CI=true && poetry run coverage run --source app/ -m pytest --disable-warnings
    poetry run coverage xml
    poetry run coverage html
    poetry run coverage report -m
elif [ $1 == "update" ];
then
    poetry show --outdated | grep --file=<(poetry show --tree | grep '^\w' | cut -d' ' -f1)
elif [ $1 == "export" ];
then
    poetry export --without-hashes --without-urls | awk '{ print $1 }' FS=';' > requirements.txt
else
    echo "Command not found"
fi
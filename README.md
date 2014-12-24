42-test template
===========================

A Django 1.6.7 project template

Use fortytwo_test_task.settings when deploying with getbarista.com

If you want to run functional tests on deployment server use next manage
command:

python manage.py test functional_tests/ --liveserver=fortytwotesttask-47.c1f3r.at.getbarista.com

### Recomendations
* apps in apps/ folder
* use per-app templates folders
* use per-app static folders
* use migrations
* use settings.local for different environments
* common templates live in templates/
* common static lives in assets/
* management commands should be proxied to single word make commands, e.g make test


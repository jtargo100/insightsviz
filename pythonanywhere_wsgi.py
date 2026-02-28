"""
PythonAnywhere WSGI Configuration
===================================
Point your PythonAnywhere web app "WSGI configuration file" to this file,
or copy its contents into the auto-generated WSGI file on PythonAnywhere.

Replace '/home/insightsvisualization/' with your actual PythonAnywhere home directory.
"""

import os
import sys

# Add your project directory to the sys.path
project_home = '/home/insightsvisualization/insightsvisualization/src'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'insightsvisualization.website.settings'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'insightsvisualization.pythonanywhere.com'

# Activate your virtual environment
virtualenv_home = '/home/insightsvisualization/.virtualenvs/insightsvisualization'
activate_this = os.path.join(virtualenv_home, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    exec(open(activate_this).read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()

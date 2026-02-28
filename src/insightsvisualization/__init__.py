import os
import sys


def main() -> None:
    """Run Django management commands."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insightsvisualization.website.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

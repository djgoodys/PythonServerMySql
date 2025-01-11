import os
import sys
#from dotenv import load_dotenv
import sys

root_path = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, os.path.join(root_path, 'mysite'))
sys.path.insert(0, root_path)

#load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PythonServerMySql.settings')

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

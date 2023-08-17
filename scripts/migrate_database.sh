CURRENT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

source ./activate.sh

python "$CURRENT_PATH/../app/manage.py" makemigrations
python "$CURRENT_PATH/../app/manage.py" migrate


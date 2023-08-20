CURRENT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

source ./activate.sh

DJANGO_SUPERUSER_PASSWORD='password' \
python "$CURRENT_PATH/../app/manage.py" createsuperuser \
    --noinput \
    --username "dev" \
    --email "dev@text.com"


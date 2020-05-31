rm -rf ./compayu/migrations
rm -rf ./user/migrations
python manage.py makemigrations user
python manage.py makemigrations compayu
python manage.py migrate user --database=db_compayu
python manage.py migrate compayu --database=db_compayu
python manage.py migrate user
python manage.py migrate compayu
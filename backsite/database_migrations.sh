rm -rf ./compayu/migrations
rm -rf ./user/migrations
mkdir ./compayu/migrations
mkdir ./user/migrations
touch ./compayu/migrations/__init__.py
touch ./user/migrations/__init__.py
python manage.py makemigrations user
python manage.py makemigrations compayu
python manage.py migrate user --database=db_compayu
python manage.py migrate compayu --database=db_compayu
python manage.py migrate user
python manage.py migrate compayu
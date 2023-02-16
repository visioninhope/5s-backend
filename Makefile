migrate:
	python manage.py makemigrations
	python manage.py migrate
run:
	python manage.py runserver
fill:
	python manage.py algorithm
	python manage.py createadmin
all:
	make migrate
	make fill
	make run
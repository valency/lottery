APP_LIST=lottery_alias lottery_market

.PHONY: init start

init:
	@python3 manage.py makemigrations $(APP_LIST)
	@python3 manage.py migrate

start:
	@python3 manage.py runserver 0.0.0.0:9003
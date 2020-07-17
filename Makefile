help:
	@echo "Targets:"
	@echo "    make run_server"
	@echo "    make run_wsgi"
	@echo "    make test"
	@echo "    make migrations"
	@echo "    make migrate"
	@echo "    make static_files"
	@echo "    make remove_pycache"

run_server:
	docker-compose up -d db
	python manage.py runserver

run_wsgi:
	 uwsgi --http :8000 \
		--http-keepalive \
		--wsgi-file config/wsgi.py \
		--static-map /static=/opt/app/staticfiles \
		--logto /dev/stdout \
		--logto2 /dev/stderr

test:
	docker-compose run -d db
	pytest

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

static_files:
	python manage.py collectstatic --no-input -v 0


remove_pycache:
	find . -name "__pycache__" -type d -exec rm -r "{}" \;

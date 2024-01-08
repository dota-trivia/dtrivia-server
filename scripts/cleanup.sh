rm -rf ./**/migrations && \
python manage.py makemigrations hero minigame && \
python manage.py migrate && \
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('devbaraus', 'me@baraus.dev', 'admin1234')"


#python manage.py upsert_heroes

FROM python:alpine3.18
WORKDIR /api

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install gunicorn
EXPOSE 8000
CMD python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:8000

FROM nginx:alpine
COPY --from=app /api /api
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
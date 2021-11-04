# api-django-app
Skeleton for django rest app
### Use on dev (if you have minikube-dev-stack)
- Deploy app on your dev cluster
```
../minikube-dev-stack/helper.sh -b -i api-django-app
```
- Note that this image does not use root so if you need to do any modifications that would require root privileges then use docker in minikube
```
minikube ssh
docker exec -ti -uroot django_app_container_in_minikube sh
```
- In case you need to run action that performs file changes (which will be disallowed by default) you can change owner for directory where this happens
```
chown 1010:1010 directory_that_will_be_mounted
```
- Note that django creates static files for admin and api views, so you need to collect them if you plan to serve them using proxy server (this will populate `./assets` directory)
```
kubectl exec -ti api_django_app_pod -- sh
python manage.py collectstatic
```
- In order to rebuild these values you need to make sure container has permissions to do it
```
chown 1010:1010 ./assets
```
- Assumption here is that this repo is an api only so there should not be any more static files
### Check (this is just to confirm if everything works as expected in case there are some issues)
- Comment out DATABASES section from `source.settings.py`
- Comment out CACHES section from `source.settings.py`
- Build image and run api-django-app on testnetwork
```
docker build -t api-django-app .
docker network create --driver=bridge testnetwork
docker run -d -p 8000:8000 --network=testnetwork -e DEBUG=True -e SELF_IP=127.0.0.1 -e SECRET_KEY=some_secret -e WHITELISTED_DOMAIN=api.django.app.localhost -e NETWORK_CHECK_URL=http://127.0.0.1:8000/ --name=api-django-app api-django-app python /app/manage.py runserver 0.0.0.0:8000
```
- Add to your `/etc/hosts`
```
127.0.0.1 api.django.app.localhost
```
- You should be able to visit in your browser
```
http://api.django.app.localhost:8000/
http://127.0.0.1/
http://api.django.app.localhost:8000/health/
http://127.0.0.1/health/
```
- You should see that `service_status` is `True` if app is accessible
- You should see that `network_status` is `False` because call to `/` returns empty json array `{}` which does not satisfy checks done by the application
- You should see that `database_status` is `False` because database section is commented out and the check done by the application will fail
- You should see that `cache_status` is `True` even though its section is commented out, it is because django uses default local memory caching in such case
- Note that if you want to test database and different cache in docker you may want to deploy corresponding services to `testnetwork` and provide proper environmental variables
- Once done testing remove container and network
```
docker container rm --force $(docker container ls -qa)
docker network rm testnetwork
```
- Remove from your `/etc/hosts`
```
127.0.0.1 api.django.app.localhost
```
- Uncomment DATABASES secion in `source/settings.py`
- Uncomment CACHES secion in `source/settings.py`
- Rebuild the image

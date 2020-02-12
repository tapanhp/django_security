# django_security

All the things related to security in Django projects



Auth0 retrieve access_token:

curl --request POST   --url 'auth0 url for token'   --header 'content-type: application/x-www-form-urlencoded'   --data grant_type=client_credentials   --data 'client_id=your_client_id'   --data client_secret=your_client_secret   --data audience=audience_url
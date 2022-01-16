### Running app:
> 1. Create .env file in the project root from ```.env.example```
> 2. Run command ```docker-compose --profile main up -d```
 
API address and port: ```http://127.0.0.0:8010``` (or other IP where the docker is running)

Available endpoints:
> Auth:
> * ```POST /api/v1/auth/register/``` - register user
> * ```POST /api/v1/auth/token/``` - obtain auth token (for protected APIs pass the token in ```Authorization``` header: ```Token mytoken```)
> * ```POST /api/v1/auth/logout/``` - invalidate auth token

> Quotes:
> * ```POST /api/v1/quotes/``` - retrieve quotes from alphavantage save to db and return them
> * ```GET /api/v1/quotes/``` - get latest quotes from db

Flower address and port: ```http://127.0.0.0:5560``` (or other IP where the docker is running)
    
### Testing app:
> 1. Create .env file in the project root from ```.env.example```
> 2. Run command ```docker-compose --profile tests up```
    
### Notes:
> * In order to protect APIs I created simple registration and auth. 
> * If the app would be a microservice it would be nicer to authenticate against JWT token, issued by auth server.
> * List of quote pairs that is retrieved from alphavantage and returned by the ```/api/v1/quotes/``` is configurable in settings.ALPHAVANTAGE_LOAD_CURRENCY_EXCHANGE_RATE_PAIRS

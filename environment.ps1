# Environment setup for powershell users
$env:POSTGRES_USER="postgres"
$env:FLASK_ENV="development"
$env:POSTGRES_PASSWORD="admin"
$env:DATABASE_URL="postgresql://postgres:admin@localhost:5432/geonames"
$env:DATABASE_URL_TEST="postgresql://postgres:admin@localhost:5432/geonames_test"
$env:GEONAMES_DATA="allCountries"
$env:APP_SETTINGS="config.DevelopmentConfig"
$env:SECRET_KEY="houdini"
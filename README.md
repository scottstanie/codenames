![](codenames/static/codenames/images/codenames.jpg)

### To run locally:

```bash
git clone https://github.com/scottstanie/codenames.git && cd codenames
mkvirtualenv codenames
pip install -r requirements.txt
./manage.py runserver
```

...this will fail, since the database needs to be set up.

#### Database setup
If you don't have postgres installed locally: http://postgresapp.com/ or `brew install postgres` (I used the former)

Open up psql

```sql
CREATE DATABASE codenames;
```

Then run the migrations to set up the database:

```bash
./manage.py migrate
```

To load the words being used:

```bash
./manage.py loaddata codenames/data/word_fixture.json
```

Now the `./manage.py runserver` should work. You will still need to make some users, so you should probably make yourself as a superuser:

```bash
./manage.py createsuperuser
```

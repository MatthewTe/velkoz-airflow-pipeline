# Importing 3rd party packages:
from sqlalchemy import create_engine

# Importing local packages:
from django.db import models

class ExternalDatabase(models.Model):
    """
    A django database model that is meant to represent an external database that
    the application is connected to.

    The method’s primary purpose is two fold:

    * It is used to dynamically generate front-end elements based on collected
        database metadata.

    * It is used to create a database URI which is used by various APIs to connect
        and extract data from said database.

    The __str__ internal method is also used to dynamically create front-end hrefs
    based on the associated name (same as the __str__ value) django view name.
    eg: {% url 'example_django_view_name_containing__str__' %}.


    A database URI is structured as follows:
    [database_type]://[username]:[password]@[host]:[port]/[database_name]

    Attributes:
        db_type (models.CharField): A string meant to represent the database type.

        user (models.CharField): A string representing a username for an account
            of the database represented by the model instance.

        password (models.CharField): A string representing the password for the
            database represented by the model instance. # TODO: Make this secure as a hashed password.

        host (models.CharField): A string representing the host of the database
            represented by the model instance. The host is either a direct string
            eg: 'localhost' or a string such as '127.0.0.1:8000'.

        port (models.CharField): A string representing the port of the
            database represented by the model instance. Port Numbers are between
            0 - 65535. Ports are stored as a string because database URIs are
            compiled as a string.

        db_name (models.CharField): A string representing the specific database name
            for the specific database represented by the model instance.

    """
    db_type = models.CharField(
        max_length = 20,
        choices = (
            ('postgres','PostgreSQL'),
            ('sqlite', 'SQLite')),
        verbose_name = 'Database Type',
        blank = True,
        help_text = "The Type of the Database being connected to.")

    user = models.CharField(
        max_length = 225,
        verbose_name = 'Database Account Username',
        blank = True,
        help_text = "The username of the account being used to connect to a database.")

    password = models.CharField(
        max_length = 225,
        verbose_name = 'Database Account Password',
        blank = True,
        help_text = "The password of the account being used to connect to a database.")

    host = models.CharField(
        max_length = 50,
        verbose_name = "Database Host",
        blank = True,
        help_text = "The host of the database being connected to.")

    port = models.CharField(
        max_length = 5,
        verbose_name = "Database Port",
        blank = True,
        help_text = "The port number of the database being connected to.")

    db_name = models.CharField(
        max_length = 225,
        verbose_name = "Database Name",
        blank = True,
        help_text = "The name of the specific database being connected to.")

    # Method that compiles a full database URI:
    def build_db_uri(self):
        """
        A method that compiles all of the necessary ExternalDatabase model fields
        into a complete database URI in the form:

        [database_type]://[username]:[password]@[host]:[port]/[database_name]

        Returns:
            str: The database URI string that is used to connect to a database.

        """
        # Compiling the database URI:
        db_uri = f"{self.db_type}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

        return db_uri

    # Method that extracts the current database status:
    def get_db_status(self):
        """
        This method attempts to connect to the database via the URI compiled by
        the internal method .get_db_uri() and an sqlalchemy engine object.

        If the connection is successful the connection is immediately closed.
        The method then returns a boolean indicating if a connection to the database
        was successful.

        Returns:
            bool: The boolean indicating if the connection to a database was successful.

        """
        # Using internal method to compile database URI:
        db_uri = self.build_db_uri()

        try:
            # Attempting to connect to the database via sqlalchemy:
            test_engine = create_engine(db_uri)
            test_conn = test_engine.connect()

            # Closing connection to db:
            test_conn.close()
            test_engine.dispose()

            return True

        except:
            False

    # Method that extracts the size of a database:
    def get_db_size(self):
        """
        This method performs a standard SQL query based on the database type that
        extracts the size of the database. The results of this query are then
        formatted and returned in bytes.

        Returns:
            int: The size of the database in bytes.

        """
        # Creating connection to the database based on a database uri:
        db_uri = self.build_db_uri()

        # Creating and opening connection to database:
        engine = create_engine(db_uri)
        con = engine.connect()

        # Creating the query based on the type of database:
        # NOTE:  Currently Database model ONLY supports PostgreSQL
        if self.db_type == 'postgres':

            db_size_query = f"SELECT pg_database_size('{self.db_name}');"

        else:
            db_size_query = None

        # Performing query if database type is supported:
        if db_size_query != None and self.get_db_status() is True:

            # Executing database query:
            query_result_set = con.execute(db_size_query)

            # Extracting result value from the result set:
            database_size = query_result_set.fetchall()[0][0]

            return database_size

        return None

    # Dunder methods:
    def __str__(self):
        return f"{self.db_type}_{self.db_name}"

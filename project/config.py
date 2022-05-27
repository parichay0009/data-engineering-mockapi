class Config:
    """
    This class stores the configuration values

    :SQLALCHEMY_DATABASE_URI = Database URI for postgresql
    """

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://db_user:db_password@spark-tech-db-postgres:5432/spark_net"
    )

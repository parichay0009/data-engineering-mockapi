import json
import requests

from sqlalchemy.sql import text

from models import DBINIT


def etl():
    """
    This method calls the users and message api using HTTPS request,load into json,transform the data
    and insert/update the data into database
    """
    engine = DBINIT().engine

    # Calling user api
    users_req = requests.get(
        "https://619ca0ea68ebaa001753c9b0.mockapi.io/evaluation/dataengineer/jr/v1/users"
    )
    user_json = json.loads(users_req.text)
    user_dict = {}
    for user in user_json:
        user_dict["id"] = user["id"]
        user_dict["first_name"] = user["firstName"]
        user_dict["last_name"] = user["lastName"]
        user_dict["birth_date"] = user["birthDate"]
        user_dict["email"] = user["email"]
        user_dict["city"] = user["city"]
        user_dict["gender"] = user["profile"]["gender"]
        user_dict["income"] = user["profile"]["income"]
        user_dict["profession"] = user["profile"]["profession"]
        user_dict["zip_code"] = user["zipCode"]
        user_dict["is_smoking"] = user["profile"]["isSmoking"]
        user_dict["created_at"] = user["createdAt"]
        user_dict["updated_at"] = user["updatedAt"]

        # connect to database insert/update the user information based on updated_at value
        with engine.connect() as conn:
            user_sql = text(
                """INSERT INTO users 
            VALUES(:id,:first_name,:last_name,:birth_date,:email,:city,:gender,:income,:profession,
            :zip_code,:is_smoking,:created_at,:updated_at)
            ON CONFLICT (id) 
            DO
            UPDATE SET 
            id=:id,first_name=:first_name,last_name=:last_name,birth_date=:birth_date,email=:email,
            city=:city,gender=:gender,income=:income,profession=:profession,
            zip_code=:zip_code,is_smoking=:is_smoking,created_at=:created_at,updated_at=:updated_at 
            where users.updated_at <> :updated_at
            """
            )
            conn.execute(user_sql, user_dict)

        for subs in user["subscription"]:
            sub_dict = {}
            sub_dict["amount"] = float(subs["amount"])
            sub_dict["created_at"] = subs["createdAt"]
            sub_dict["end_date"] = subs["endDate"]
            sub_dict["start_date"] = subs["startDate"]
            sub_dict["status"] = subs["status"]
            sub_dict["user_id"] = user["id"]

            # connect to database insert/update the subscription for every user based on user_id and created_at.
            with engine.connect() as conn:
                sub_sql = text(
                    """INSERT INTO subscriptions 
                VALUES(:user_id,:created_at,:amount,:status,:start_date,:end_date)
                ON CONFLICT (user_id,created_at) 
                DO
                UPDATE SET 
                amount = :amount,status=:status,user_id=:user_id,created_at=:created_at,
                start_date=:start_date,end_date=:end_date
                """
                )
                conn.execute(sub_sql, sub_dict)

    # Calling messages api
    message_req = requests.get(
        "https://619ca0ea68ebaa001753c9b0.mockapi.io/evaluation/dataengineer/jr/v1/messages"
    )
    msg_json = json.loads(message_req.text)
    msg_dict = {}
    for msg in msg_json:
        msg_dict["id"] = msg["id"]
        msg_dict["message"] = msg["message"]
        msg_dict["sender_id"] = msg["senderId"]
        msg_dict["receiver_id"] = msg["receiverId"]
        msg_dict["created_at"] = msg["createdAt"]

        # connect to database insert/update the message based on message id.
        with engine.connect() as conn:
            msg_sql = text(
                """INSERT INTO messages 
                VALUES(:id,:message,:sender_id,:receiver_id,:created_at)
                ON CONFLICT (id) 
                DO
                NOTHING
                """
            )
            conn.execute(msg_sql, msg_dict)


etl()

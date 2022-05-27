/* How many total messages are being sent every day? */

with msgs as(
    select id,created_at from messages
),
dates as(
    select to_char(created_at::date,'YYYY-MM-DD') as date1,count(id) 
    over(partition by to_char(created_at::date,'YYYY-MM-DD')) as no_of_msg,
    row_number() over(partition by to_char(created_at::date,'YYYY-MM-DD')) as rnk
    from msgs
)
select date1,no_of_msg from dates where rnk=1;

/* Are there any users that did not receive any message? */

select id,first_name,last_name from users where id not in (select DISTINCT receiver_id from messages);

/* How many active subscriptions do we have today? */

with join_t as(
    select usr.id,sub.status,end_date from users as usr join subscriptions as sub on usr.id=sub.user_id 
)
select count(id) as active_users from join_t where status='Active' and end_date::date>=CURRENT_DATE::date ;

/* Are there users sending messages without an active subscription? */

with cte1 as(select sub.user_id,msg.sender_id,sub.end_date,msg.created_at,sub.status,sub.start_date
from messages as msg left join subscriptions as sub on msg.sender_id=sub.user_id),
cte2 as(
select * from cte1 where 
(created_at::date between start_date::date and end_date::date) or status is null
)
select DISTINCT sender_id from cte2 where status <> 'Active' or status is null
EXCEPT
select DISTINCT sender_id from cte2 where status='Active';

/* There are some data for users where location information like city,zip_code is not avialable also 
the gender information is required for matching there should be email validation and zip code varification
scheme.
There should be no entries of message without subscription for example sender_id 6 in message has no entiries 
in subscriptions table. 
*/

select id,first_name from users where city is null or zip_code is null or gender is null;

В этом Лабке мы решаем лабораторную задачу Академии веб-безопасности Portswigger по SQL-инъекциям под названием Conditional Responses с помощью скрипта на Python. Это слепой эксплойт для SQL-инъекций на основе булевых значений.

In the first step, I will determine the type of database by using a time-based response attack. The databases we are considering are Oracle, Microsoft SQL Server, PostgreSQL, and MySQL. 

The payload `';SELECT SLEEP(5)-- ` did not work for MySQL, but `';SELECT pg_sleep(5)-- ` (OR with url encode: `'%3bselect+pg_sleep(5)--+`) worked for PostgreSQL. This confirms that our database is PostgreSQL. 


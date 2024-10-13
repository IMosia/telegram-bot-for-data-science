# Telegram Bot for Data Science  
## What is this?  
This is a user-friendly repo which allowes one to create a personal telegram bot together with PostgreSQL database and Airflow for automatic data processing.  
Follow the instructions below, and the only thing you need to change is code to run your application.  
## Why?  
I do believe that there is a big gap between learning Data Science to extend that one can freely operate in JupyterNotebook environment and making something which actually works as application.  
Telegram bots allow developer-friendly approach which does not require specific knowledge on how Internet works or how to make a mobile app.  
At the same time it provides excelent interface which allowes to upload and recieve various data types.  
So, why not to build you first application like this?  
With simply following the instructions below and running scripts on you local machine you can app with friends and community all around the Globe.  
## What's inside?  
The proposed architecture consists of 4 services.  
1. Telegram-bot with any Python-based logic you would like to use.  
2. PostgreSQL database with persistent volume to store your data.  
3. Liquibase Script to automatically create Schema for DataBase following Infrustructre As Code principles.  
4. Apache Airflow service to perform any scheduled tasks, like data analysis, ETL pipelines, or automatic notifications.  
## How to use  
1. Fork or copy content of this repository to your github account.  
2. Run the following command on your local machine in the repository you would like to work in:  
```
git clone https://github.com/IMosia/bot_for_ds.git
```  
If you copied it to your repo, you colud get link from Code button.  
3. Make sure you have [python](https://www.python.org/downloads/) installed on your computer. 
4. Install [docker-desktop](https://www.docker.com/products/docker-desktop/), it is needed to run the application.  
5. Install [PostgreSQL command-line interface](https://www.postgresql.org/download/)  
    While installing remove installation of everything but command-line interface.  
    If you do install databse itself, please, change the DB Ports in .env file from 5432, as it will be ocupied by newly install Postgres.  
6. Create a new Bot and recieve your BotToken from [BotFather](https://telegram.me/BotFather) in Telegram (```/newbot``` command).  
7. Copy .env_example file and rename copy as .env.  
Add your needed secret infromation there, as BotToken.  
It should not be pushed to GitHub as it containes your secret infromation.  
Currently .env is in .gitignore, so this is safe automatically.
8. **Create your application!** For more details see the following section.  
9. Run the following command to start application:  
```
docker-compose up -d --build
```  
Go to interface of docker-desktop to check that all containers are working.  Liquibase container should be down after the migration is finished.  
To stop the application:  
```
docker-compose down
```  
If you would like to remove persistant volumes with logs and database data you can run  
```
docker-compose down --volumes
```  
10. ???  
11. Enjoy!

## How to create application.  
### DataBase schema  
To create Tables in the DB one need to change the following file: *liquibase/changelog/base.yaml*.  
It containes description of how the Data Schema should look like.  
In general, this is very [powerful tool](https://docs.liquibase.com/home.html) used in our case so that one does not need to create all the tables from terminal.  
While creating Schema for your data a wise idea is to make their graphical representation, using one of many available tools available for free like [this](https://dbdiagram.io/) or [that](https://drawsql.app/).  

### Telegram Bot  
Bla  
The bot is in async
# requirements.txt

### Apache Airflow  
Is one of the most popular [tools](https://airflow.apache.org/docs/apache-airflow/stable/index.html) for ETL pipelines creation and automatic analytics.  
It does allow to make regular actions, e.g. send greatings message every day, or make back-ups every Sunday.  
The options are endless - explore and enjoy it.  
The basic unit is DAG - a program to execute inside Airflow.



## Examples  
Fill free to share your results:)  


# Credentials

## server
ip-server: 10.0.0.43/24
account: antoine
password: abc123

## fossbilling
port:8080
port-databse:3306

### .env
|       FOSSBillingService/.env       |
| :---------------------------------: |
|        mysql_db=fossbilling         |
|     mysql_user=fossbilling_user     |
| mysql_password=fossbilling_password |
|       mysql_root_password='1'       |

### admin account
userName=Admin \
email=antoine.goethuys@student.ehb.be \
password=AB12cd34# \

### Currency

Code=EUR
Title=Euro
price format=€{price}

### api

key=dj2U6E5ZEowD8Em00YfnIehQGavcVOPH

#### password user generation

username = first part of email (before @)
password = username + postcode 

## wordpress

### admin cred

|   wordpress/.env   |
| :----------------: |
|   username=admin   |
| password=AB12cd34# |
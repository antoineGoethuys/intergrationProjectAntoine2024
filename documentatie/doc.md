# github url (public)
https://github.com/antoineGoethuys/intergrationProjectAntoine2024
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

# link
10.0.0.44:8080 = fossbilling
10.0.0.44:4000 = wp
10.0.0.44:15672 = rabbitmq

# ports
8080 = fossbilling
4000 = wp
15672 = rabbitmq

# to do list[*](todo.md)

## todo

- [ ] data struc product
- [ ] write test
    - [ ] wp user create
    - [ ] wp user update
    - [ ] wp user delete
    - [ ] fossbilling user create
    - [ ] fossbilling user update
    - [ ] fossbilling user delete
- [ ] wp product create
- [ ] wp product update
- [ ] wp product delete
- [ ] fossbilling product create
- [ ] fossbilling product update
- [ ] fossbilling product delete
- [ ] write test
    - [ ] wp product create
    - [ ] wp product update
    - [ ] wp product delete
    - [ ] fossbilling product create
    - [ ] fossbilling product update
    - [ ] fossbilling product delete
 - [ ] CI
    - [ ] auto tests
    - [ ] auto deployement
- [ ] factuur generate
- [ ] other software packet

## doing

 - [x] write docunentation
 - [x] make the analyses
 - [ ] wp user delete
 - [ ] fossbilling user create
 - [ ] fossbilling user update
 - [ ] fossbilling user delete

## done

- [x] install fossbilling
- [x] install rabbitMQ
- [x] data struc user
- [x] wp ui (view)
- [x] install wp
- [x] wp user create
- [x] wp user update

# mvp[*](what-works.md)

## what works in my project (mvp)
 - create user in foss and get it in wp
 - update user in foss and get it in wp

## what don't work (mvp)
 - delete user in foss and get it in wp

 - create user in foss and get it in wp
 - update user in foss and get it in wp
 - delete user in foss and get it in wp

# problem that i have hat or have[*](problemen.md)
## problemen onderweg
 - installatie van wordpress in docker (3-4 weken tijd)
   - moeilijk met docker syteem
 - slordigheid
 - telaat met het echt beginnen werken (midden juli)
 - installeren van de vm
   - 1e van de mijn vm
     - de schijf was super vol maar ik had in de virtual disk verander naar +40Gb maar hij wou er maar 11Gb van gebruiken dus had ik veel errors van u kunt deze file niet opslaan wegen een tekort aan plaats maar het was gewoon een print statment toegevoegd maar hij wou niet
     - dus veer tijd verloren aan die vm weer levend te maken (+- 1-2 weken) gebrobeerd
   - 2e vm is de huidige vm
 - te snel beginnen weken
   - bijna niet nagedacht hoe het werkt in de grote lijnen en dus veel tijd verspeeld aan direct beginnen werken en dus niet echt beginnen beredeneren over hoe deze zou er moeten na zijn
     - file structure
     - classdiagram
     - ...
   - dus als gevolg veel moeten proberen alles met elkaar te laten werken en dus veel debugging en dus weinig werk weergegeven
 - te veel herbegonnen met de code als gevolg van te weig bedenking over het project
 - weinig to geen veilige code (crededentials die direct in de files liggen (docker-compose, python-scripts))
 - het vergeten gebruiken van direct topic exchanges
## resultaat
 - veel van de mvp niet voldaan

### Step 1: Create a project under google developer console.

![Create Project](./screenshots/create_project/1.png)

### Step 2: Select a organization by clicking on No organization on top bar

![Select a organization](./screenshots/create_project/2.png)
![Loading Image](./screenshots/create_project/3.png)

### Step 3: Create a new project by clicking on NEW PROJECT and put all the details required

![creat new project](./screenshots/create_project/4.png)

### Congratulations Project is created!!! Dashboard of console will look like following

![Dashboard console](./screenshots/create_project/5.png)

### Step 4: Enable the APIs which are required for this application

* Calendar API (For CRUD Operations on indiviuals calendar)
![Search for calendar API](./screenshots/create_project/6.png)
![click on Enable button](./screenshots/create_project/8.png) Click on Enable button

* ADMIN SDK (For accessing resources, users and groups details) (read-only)

![Search and Enable ADMIN SDK](./screenshots/create_project/9.png) Click on Enable button

### Step 5: Create OAuth Client to access this application/project using REST APIs

![Create Credentials OAuth](./screenshots/create_project/10.png) Click on Create crendentials
![Select OAuth Client ID](./screenshots/create_project/11.png) Click on OAuthClient ID
![OAuth Client ID is Created](./screenshots/create_project/12.png) OAuth client ID is created


### Step 6: Log on to Google Admin Console To create users, groups and shared resources such as meeting rooms, cabs, play rooms, etc.

![Dashboard Admin Console](./screenshots/create_project/13.png) Google Admin Console Dashboard

### Step 7: Create some users and One admin user to access the users details and group details on your behalf and assign a custom role to this user.

![Users console](./screenshots/create_project/14.png) Users console
![Create normal user](./screenshots/create_project/16.png) Create a new user who is going to use this application
![Create admin user](./screenshots/create_project/15.png) Create a new user who will act as admin. Create the normal user only will make this user admin by assigning Admin Role.

### Step 8: Create a custom Admin Role which will access users details and groups details

![Admin Role console](./screenshots/create_project/21.png) navigate to Admin Role console Menu->Account->Admin Roles
![amdin roles console](./screenshots/create_project/18.png) click on create new role
![Creating new role](./screenshots/create_project/19.png) new role created now select privileges 
![Select privileges](./screenshots/create_project/20.png) select read-only for users, groups and resources


### Step 9: Assign this newly created role to the admin user that we have created above 

![Go to Admin roles and privileges](./screenshots/create_project/17.png) Find the role and make it enable 

## Congratulations we are all set for to Access Calendar remotely without Calendar Application

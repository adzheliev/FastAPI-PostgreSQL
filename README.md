<span style="font-family: Tahoma;"> 

## Y_lab

### To run locally

Open your IDE of choice and clone this repository

```bash
git clone https://github.com/adzheliev/Y_lab.git
```
To run **test for application**, please use following command on yor terminal

```bash
docker compose -f docker-compose-tests.yml up
```

Once tests are completed use following command on yor terminal to remove test containers
```bash
docker compose -f docker-compose-tests.yml down    
```

To run **application**, please use following command on yor terminal

```bash
docker compose -f docker-compose.yml up 
```
Once you finished testing the application use following command on yor terminal to remove containers
```bash
docker compose -f docker-compose.yml down    
```

Query to get dishes count and submenus count of the certain menu is realized in
```bash
/routes/menu.py
```

The query is following:
```bash

menu = db.query(Menu.id, 
                Menu.title, 
                Menu.description, 
                func.count(Submenu.id).label('submenus_count'),
                func.count(Dish.id).label('dishes_count')).
                outerjoin(Submenu, Submenu.menu_id == Menu.id).
                outerjoin(Dish, Dish.submenu_id == Submenu.id).
                filter(Menu.id == target_menu_id).
                group_by(Menu.id).
                first()
```

</span>

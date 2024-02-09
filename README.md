<span style="font-family: Tahoma;"> 

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

</span>

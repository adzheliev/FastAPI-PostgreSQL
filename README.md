## Y_lab step 1

### To run locally

Open your IDE of choice and clone this repository

```bash
git clone https://github.com/adzheliev/Y_lab.git
```
From project directory create a virtual env with following command in yor terminal

```bash
python3 -m venv .venv   
```

And activate virtual env with following command in yor terminal
```bash
source ./venv/bin/activate    
```

Install dependencies with following command in yor terminal

```bash
pip install -r requirements.txt
```
Once all is installed, run the app with following command in yor terminal
```bash
uvicorn main:app --reload
```    
Now the app is running. Swagger documentation is available on
```bash
http://127.0.0.1:8000/docs
```  

Feel free to test it or import tests file (attached) in your postman 

.env file is available for testing purposes
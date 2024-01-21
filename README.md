## Test task for Simple Solutions

For task please see TASK.md

Application is running on http://16.171.151.22:8000

### Setup locally

Open your IDE of choice and clone this repository

```bash
git clone https://github.com/adzheliev/simple_solution
```

or use SSH keys

```bash
git clone git@github.com:adzheliev/simple_solution.git
```

Register your Stripe account on https://stripe.com

Use docker build command to build images inserting your stripe keys in it. Make sure your docker is installed and ready to be used

```bash
docker build --build-arg STRIPE_PUBLISHABLE_KEY=<insert here your key> \                                       ─╯
--build-arg STRIPE_SECRET_KEY=<insert here your key> \
--build-arg DJANGO_SECRET_KEY='django-insecure-ze*ut341u7$hyp$7ys5a)fs$x%trly%=d$-h$wv0=apc&)j^#m' \
-t myapp .

```

Use docker run command

```bash
docker run -p 8000:8000 myapp  
```

### Setup on AWS EC2

Once you created EC2 instance on AWS (t2.micro in more than enough), please follow next steps

Update the System
```bash
sudo apt-get update
```
To get this repository, run the following command inside your git enabled terminal
```bash
git clone https://github.com/adzheliev/simple_solution
```
You will need django to be installed in you computer to run this app. Head over to https://www.djangoproject.com/download/ for the download guide

Download django usig pip
```bash
sudo apt install python3-pip -y
```
```bash
pip install -r requirements.txt
```

Add your EC2 public IPv4 address to setting.py in 

```
ALLOWED_HOSTS = ['127.0.0.1', <your IP>]
```
Do the same in api.views.py. (you can use vim for that)

Modify your instance inbound security rules allowing access from Custom TCP through port 8000 to 0.0.0.0/0

Once you have installed dependencies, go to the cloned repo directory and run the following command

```bash
python3 manage.py makemigrations
```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command
```bash
python3 manage.py migrate
```

One last step and then our todo App will be live. We need to create an admin user to run this App. On the terminal, type the following command and provide username, password and email for the admin user
```bash
python3 manage.py createsuperuser
```

```bash
python3 manage.py runserver 0.0.0.0:8000
```

The app now in running on your EC2. You can access it on <EC2 public IPv4>:8000

Alternatively you can install Docker on your EC2 instance and launch Docker build and Docker run
commands as previously mentioned for local use.

### ToDo

1) Adding currency pair
2) Adding custom Tax and Discount to Checkout session and then make them available in checkout form
3) Switch to Stripe Payment Intent instead of Stripe Session
4) Adding more friendly user interface, more items and orders.
5) Mapping IPs in order to make application available through custom link
6) Tests and exceptions catching
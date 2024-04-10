# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.fields import ArrayField


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    last_update = models.DateTimeField(auto_now_add=True)
    film = models.ManyToManyField('Film', through='FilmActor')

    class Meta:
        managed = False
        db_table = 'actor'


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=20)
    city = models.ForeignKey('City', models.DO_NOTHING)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'address'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    last_update = models.DateTimeField(auto_now_add=True,)

    class Meta:
        managed = False
        db_table = 'category'


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    country = models.ForeignKey('Country', models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'city'


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'country'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    store_id = models.SmallIntegerField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=50, blank=True, null=True)
    address = models.ForeignKey(Address, models.RESTRICT)
    activebool = models.BooleanField(default=True)
    create_date = models.DateField(auto_now_add=True)
    last_update = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


AGE_RATING =[
    ("G", "General Audiences"),
    ("PG", "Parental Guidance Suggested"),
    ("PG-13", "Inappropriate for Children Under 13" ),
    ("R", "Restricted"),
    ("NC-17", "Adults Only"),
  ]


class Film(models.Model):
    film_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    language = models.ForeignKey('Language', models.RESTRICT)
    rental_duration = models.SmallIntegerField(default=3)
    rental_rate = models.DecimalField(max_digits=4, decimal_places=2, default=4.99)
    length = models.SmallIntegerField(blank=True, null=True)
    replacement_cost = models.DecimalField(max_digits=5, decimal_places=2, default=19.99)
    rating = models.CharField(blank=True, null=True, choices=AGE_RATING, default="G",)  # This field type is a guess.
    last_update = models.DateTimeField(auto_now_add=True)
    special_features = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    fulltext = SearchVectorField()  # This field type is a guess.
    category = models.ManyToManyField(Category, through='FilmCategory')

    class Meta:
        managed = False
        db_table = 'film'


class FilmActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.RESTRICT)
    film = models.ForeignKey(Film, on_delete=models.RESTRICT)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'film_actor'
        unique_together = (('actor', 'film'),)


class FilmCategory(models.Model):
    film = models.ForeignKey(Film, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'film_category'
        unique_together = (('film', 'category'),)


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    film = models.ForeignKey(Film, models.RESTRICT)
    store_id = models.SmallIntegerField()
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'language'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.RESTRICT)
    staff = models.ForeignKey('Staff', models.RESTRICT)
    rental = models.ForeignKey('Rental', models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment'


class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True)
    rental_date = models.DateTimeField()
    inventory = models.ForeignKey(Inventory, models.RESTRICT)
    customer = models.ForeignKey(Customer, models.RESTRICT)
    return_date = models.DateTimeField(blank=True, null=True)
    staff = models.ForeignKey('Staff', models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'rental'
        unique_together = (('rental_date', 'inventory', 'customer'),)


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    address = models.ForeignKey(Address, models.RESTRICT)
    email = models.CharField(max_length=50, blank=True, null=True)
    store_id = models.SmallIntegerField()
    active = models.BooleanField(default=True)
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=40, blank=True, null=True)
    last_update = models.DateTimeField(auto_now_add=True)
    picture = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    manager_staff = models.ForeignKey(Staff, models.RESTRICT)
    address = models.ForeignKey(Address, models.RESTRICT)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'store'

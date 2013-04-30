from django.db import models

class Car(models.Model):
	model = models.CharField(max_length=500, blank=True, null=True)
	year = models.IntegerField(blank=True, null=True)
	num_miles = models.IntegerField(blank=True, null=True)
	owner = models.CharField(max_length=500, blank=True, null=True)

	def __unicode__(self):
		return self.model

class Furniture(models.Model):
	name = models.CharField(max_length=500, blank=True, null=True)
	num_legs = models.IntegerField(blank=True, null=True)
	brand = models.CharField(max_length=500, blank=True, null=True)

	def __unicode__(self):
		return self.name

class Audiobook(models.Model):
	title = models.CharField(max_length=500, blank=True, null=True)
	duration = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return self.title

class Hologram(models.Model):
	name = models.CharField(max_length=500, blank=True, null=True)
	width = models.FloatField(blank=True, null=True)
	height = models.FloatField(blank=True, null=True)
	depth = models.FloatField(blank=True, null=True)

	def __unicode__(self):
		return self.name

class ExtraAttribute(models.Model):
	model_name = models.CharField(max_length=500, null=False)
	model_id = models.IntegerField(null=False)
	attribute_name = models.CharField(max_length=500, null=False)
	attribute_value = models.CharField(max_length=500, null=False)

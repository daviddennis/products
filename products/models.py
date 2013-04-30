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

class Attribute(models.Model):
	model_type = models.CharField(max_length=500, null=False)
	name = models.CharField(max_length=500, null=False)

	def __unicode__(self):
		return "%s:%s" % (self.model_type, self.name)

class AttributeInstance(models.Model):
	attribute = models.ForeignKey(Attribute)
	model_id = models.IntegerField(null=False)
	value = models.CharField(max_length=500, null=False)

	def __unicode__(self):
		return "%s:%s:%s" % (self.attribute.model_type, self.model_id, self.value)

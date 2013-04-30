from django.db import models


class Attribute(models.Model):
	model_type = models.CharField(max_length=500, null=False)
	name = models.CharField(max_length=500, null=False)

	def __unicode__(self):
		return "%s:%s" % (self.model_type, self.name)


class Car(models.Model):
	model = models.CharField(max_length=500, blank=True, null=True)
	year = models.IntegerField(blank=True, null=True)
	num_miles = models.IntegerField(blank=True, null=True)
	owner = models.CharField(max_length=500, blank=True, null=True)

	def __unicode__(self):
		return self.model


class CarAttribute(models.Model):
	car = models.ForeignKey(Car)
	attribute = models.ForeignKey(Attribute)
	value = models.CharField(max_length=500, null=False)

	def __unicode__(self):
		return "%s:%s:%s" % (self.car.model, self.attribute.name, self.value)


class Furniture(models.Model):
	name = models.CharField(max_length=500, blank=True, null=True)
	num_legs = models.IntegerField(blank=True, null=True)
	brand = models.CharField(max_length=500, blank=True, null=True)

	def __unicode__(self):
		return self.name


class FurnitureAttribute(models.Model):
	furniture = models.ForeignKey(Furniture)
	attribute = models.ForeignKey(Attribute)
	value = models.CharField(max_length=500, null=False)

	def __unicode__(self):
		return "%s:%s:%s" % (self.furniture.name, self.attribute.name, self.value)


class Audiobook(models.Model):
	title = models.CharField(max_length=500, blank=True, null=True)
	duration = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return self.title


class AudiobookAttribute(models.Model):
	audiobook = models.ForeignKey(Audiobook)
	attribute = models.ForeignKey(Attribute)
	value = models.CharField(max_length=500, null=False)

	def __unicode__(self):
		return "%s:%s:%s" % (self.audiobook.name, self.attribute.name, self.value)


class Hologram(models.Model):
	name = models.CharField(max_length=500, blank=True, null=True)
	width = models.FloatField(blank=True, null=True)
	height = models.FloatField(blank=True, null=True)
	depth = models.FloatField(blank=True, null=True)

	def __unicode__(self):
		return self.name


class HologramAttribute(models.Model):
	hologram = models.ForeignKey(Hologram)
	attribute = models.ForeignKey(Attribute)
	value = models.CharField(max_length=500, null=False)

	def __unicode__(self):
		return "%s:%s:%s" % (self.hologram.name, self.attribute.name, self.value)


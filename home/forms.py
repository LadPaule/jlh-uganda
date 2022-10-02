from django.forms import CharField, EmailField, FloatField, Form

class DonateForm(Form):
  name = CharField(label="Your Name", max_length=500)
  email= EmailField()
  phone = CharField(max_length=20)
  amount = FloatField()
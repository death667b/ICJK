from .models import Car
from django.shortcuts import render
from django.db.models import Q

class CarView():
    def __init__(self, db_id):
        self.id = db_id
        self.model = Car.objects.filter(Q(id=db_id))
    
    def render(self, request):
        return None


class CommercialCarView(CarView):
    def __init__(self, db_id):
        super(CommercialCarView, self).__init__(db_id)
    
    def render(self, request):
        return render(request, 'Home/car.html')

class PersonalCarView(CarView):
    def __init__(self, db_id):
        super(PersonalCarView, self).__init__(db_id)

    def render(self, request):
        return render(request, 'Home/car.html', {"car":self.id})

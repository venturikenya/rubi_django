from background_task import background
from .models import Food
@background(5)
def clear_offers():
    items_onOffer=Food.objects.filter(on_offer=True)
    for item in items_onOffer:
        item.on_offer=False
        print(str(item.food_name)+'has been cleared')

#def mail_new_user()

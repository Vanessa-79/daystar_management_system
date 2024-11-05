from django import template
import pytz
from datetime import datetime

register = template.Library()

@register.simple_tag #transform current time
def current_time_eat():
    eat = pytz.timezone('Africa/Nairobi')
    eat_time = datetime.now(eat)
    return eat_time.strftime('%A, %B %d, %Y | %I:%M %p')

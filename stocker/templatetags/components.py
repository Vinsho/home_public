from django import template

register = template.Library()


@register.inclusion_tag("stocker/stock_card.html")
def stock_card(article):
    return {
        'article': article
    }


@register.inclusion_tag("stocker/impact.html")
def impact(impact):
    return {
        'impact': impact
    }


@register.inclusion_tag("klcovany/device_card.html")
def device_card(device, priority_range):
    return {
        'device': device,
        'priority_range': priority_range
    }

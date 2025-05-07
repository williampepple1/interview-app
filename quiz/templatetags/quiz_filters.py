from django import template

register = template.Library()

@register.filter
def filter_by_assessment(user_assessments, assessment):
    """
    Filter user assessments by assessment and return the first match or None.
    """
    return user_assessments.filter(assessment=assessment).first() 
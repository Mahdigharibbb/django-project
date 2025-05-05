from django.db.models.signals import pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from .models import Product
from django.core.mail import send_mail


@receiver(pre_save, sender=Product)
def calculate_new_price(sender, instance, **kwargs):
    instance.new_price = instance.price - instance.off


@receiver(m2m_changed, sender=Product.likes.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(post_delete, sender=Product)
def users_like_changed(sender, instance, **kwargs):
    author = instance.author
    subject = "your post has been delete"
    message = f"your post has been delete (Id{instance.id})"
    send_mail(subject, message, 'mahdi.gharib1386@gmail.com', [author.email], fail_silently=False)


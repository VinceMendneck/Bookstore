import factory
from product.models import Product, Category

class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('word')
    slug = factory.Faker('slug')
    description = factory.Faker('text', max_nb_chars=500)
    active = True

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.Faker('random_int', min=1, max=1000)
    title = factory.Faker('word')
    
    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.category.add(category)
        
    class Meta:
        model = Product
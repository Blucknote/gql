import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from graphene_django.types import DjangoObjectType

from .models import Publish, Category, Comment


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class CategoryInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class PublishNode(DjangoObjectType):
    class Meta:
        model = Publish
        filter_fields = ['text', 'published']
        interfaces = (relay.Node, )


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class PublishGQ(graphene.ObjectType):
    text = graphene.String()
    published = graphene.Boolean()
    categories = graphene.List(graphene.Int)


class CommentGQ(graphene.ObjectType):
    text = graphene.String()
    published = graphene.Boolean()
    publish = graphene.Int()


class PublishInput(graphene.InputObjectType):
    text = graphene.String()
    published = graphene.Boolean()
    categories = graphene.List(graphene.Int)


class CreatePublish(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        published = graphene.Boolean()
        categories = graphene.List(graphene.Int)

    publish = graphene.Field(lambda: PublishGQ)

    def mutate(root, info, text, categories, published=False):
        publish = Publish.objects.create(
            text=text,
            published=published
        )
        cats = Category.objects.filter(
            id__in=categories
        )
        publish.categories.set(cats)
        publish.save()
        return CreatePublish(publish=publish)


class CreateComment(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        published = graphene.Boolean()
        publish = graphene.ID()

    comment = graphene.Field(CommentGQ)

    def mutate(root, info, text, publish, published=False):
        publish = Publish.objects.get(id=publish)
        comment = Comment.objects.create(
            text=text,
            published=published,
            publish=publish
        )
        comment.save()
        return CreateComment(comment=comment)


class MyMutations(graphene.ObjectType):
    create_publish = CreatePublish.Field()
    create_comment = CreateComment.Field()


class Query(object):
    all_categories = graphene.List(CategoryType)

    publishes = relay.Node.Field(PublishNode)
    all_publishes = DjangoFilterConnectionField(PublishNode)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_publishes(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Publish.objects.prefetch_related('categories').all()



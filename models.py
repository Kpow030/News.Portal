from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum




# Модель Author
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
# Связь «один к одному» с встроенной моделью пользователей User;
# рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
# Имеет единственное поле: название категории. Поле должно быть уникальным
# (в определении поля необходимо написать параметр unique = True


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


# Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
# связь «один ко многим» с моделью Author;
# поле с выбором — «статья» или «новость»;
# автоматически добавляемая дата и время создания;
# связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
# заголовок статьи/новости;
# текст статьи/новости;
# рейтинг статьи/новости.


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    News = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (News, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dataCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


# Модель PostCategory
# Промежуточная модель для связи «многие ко многим»:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» с моделью Category


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


# Модель Comment
# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
# текст комментария;
# дата и время создания комментария;
# рейтинг комментария.


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

# Create your models here.

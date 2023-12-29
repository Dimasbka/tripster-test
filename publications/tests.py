from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .models import Publication, PublicationVote
from .views import publications_listing, publication_add, vote_add, vote_delete

class PublicationTestCase(TestCase):
    def setUp(self):
        """ как тесты выполняются в случайном порядкедля 
            сразу создаю пара пользователей и публикацию 
            + для тестов вьюшек нужна фабрика для запросов
        """ 
        self.autor = User.objects.create_user(
            username="autor", email="autor@test.com", password="top_secret"
        )

        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="top_secret"
        )

        self.publication1 = Publication.objects.create(
                text='Публикация для тестов оценок',
                user = self.autor
                )

        self.factory = RequestFactory()

# эмулируем запросы для залогиненного пользователя
    def test_publications_listing_for_logged_in_user(self):
        """  список публикаций для залогиненного пользователя""" 
        request = self.factory.get("")
        request.user = self.autor
        listing_response = publications_listing( request )
        self.assertEqual(listing_response.status_code, 200 ) 


    def test_publication_add_for_logged_in_user(self):
        """  добавление ппубликации для залогиненного пользователя""" 
        request = self.factory.post(
            "/publication/add/",
            data={ 'text':'Текст публикации 1' }
        )
        request.user = self.autor
        add_response = publication_add( request )
        self.assertRedirects(add_response, "/", fetch_redirect_response=False)


    def test_vote_add_for_logged_in_user(self):
        """  оценка публикации для залогиненного пользователя """ 
        request = self.factory.post(
            "/publication/vote/",
            data={ "publication_id":self.publication1.id,"vote":1},
            content_type='application/json',
        )
        request.user = self.user
        vote_response = vote_add( request )
        self.assertContains(vote_response, b'"status": "added"' ) 

        # повторная оценка публикации 
        
        vote_response2 = vote_add( request )
        self.assertContains(vote_response2, b'"status": "pass"' ) 


# эмулируем запросы для гостя
    def test_publications_listing_for_anonymous_user(self):
        """  список публикаций для гостя """ 
        request = self.factory.get("")
        request.user = AnonymousUser()
        listing_response = publications_listing( request )
        self.assertEqual(listing_response.status_code, 200 )


    def test_publications_listing_for_anonymous_user(self):
        """  добавления публикации - должно вызывать редирект на страницу логина """ 
        request = self.factory.post(
            "/publication/add/",
            data={ 'text':'Текст публикации 2' }
        )
        request.user = AnonymousUser()
        add_response = publication_add( request )
        self.assertRedirects(add_response, 
                             "/accounts/login/?next=/publication/add/", 
                             fetch_redirect_response=False)


    def test_publications_listing_for_anonymous_user(self):
        """  оценка  публикации - должно вызывать редирект на страницу логина """ 
        request = self.factory.post(
            "/publication/vote/",
            data={ "publication_id":self.publication1.id,"vote":1},
            content_type='application/json',
        )
        request.user = AnonymousUser()
        vote_response = vote_add( request )
        self.assertRedirects(vote_response, 
                             "/accounts/login/?next=/publication/vote/", 
                             fetch_redirect_response=False)


    def test_vote_update_logic(self):
        """ Проверка правильности подсчета голосов, здесь для полуление свежего 
        рейтингаиспользую метод класса get_votes_rating_dict """


        # создаю новую публикацию
        publication = Publication.objects.create(
                text='Публикация для тестов логики оценок',
                user = self.autor
                )
        publication_id = publication.id


        # 2 одинаковых голоса
        PublicationVote.vote_add_or_update( publication_id, 1, self.autor.id )
        PublicationVote.vote_add_or_update( publication_id, 1, self.user.id  )
        res =  Publication.get_votes_rating_dict( publication_id )
        self.assertEqual(res, {'votes': 2, 'rating': 2} ) 


        # один из пользователей удалил свой голос
        PublicationVote.vote_delete( publication_id, self.user.id )
        res =  Publication.get_votes_rating_dict( publication_id )
        self.assertEqual(res, {'votes': 1, 'rating': 1} ) 


        # 2 разных голоса
        PublicationVote.vote_add_or_update( publication_id, -1, self.user.id )
        res =  Publication.get_votes_rating_dict( publication_id )
        self.assertEqual(res, {'votes': 2, 'rating': 0} ) 
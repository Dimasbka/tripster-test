# Create your tests here.
from django.test import TestCase,  Client
from django.contrib.auth.models import  User
from publications.models import Publication



class ApiTestCase(TestCase):
    def setUp(self):
        """ как тесты выполняются в случайном порядкедля 
            сразу создаю пара пользователей и публикацию 
            + для тестов API нужна фабрика для запросов
        """ 
        self.autor = User.objects.create_user(
            username="autor", email="autor@test.com", password="autor"
        )

        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="user"
        )

        self.publication1 = Publication.objects.create(
                text='Публикация для тестов оценок',
                user = self.autor
                )



# эмулируем запросы для залогиненного пользователя
    def test_API_publications_listing_for_logged_in_user(self):
        """  список публикаций для залогиненного пользователя""" 
        c = Client()
        c.login(username="autor", password="autor")
        listing_response = c.get(
                "/api/publications/",
            )
        self.assertEqual(listing_response.status_code, 200 )


    def test_API_publication_add_for_logged_in_user(self):
        """  добавление ппубликации для залогиненного пользователя""" 
        c = Client()
        c.login(username="autor", password="autor")
        add_response = c.post(
                "/api/publications/",
                data={ 'text':'Текст публикации 1' },
                headers={' Content-Type':'application/json' },
            )
        self.assertEqual(add_response.status_code, 201 )
        self.assertEqual(add_response.status_code, 201 ) 


    def test_API_publications_vote_for_logged_in_user(self):
        """  оценка публикации для залогиненного пользователя """ 
        c = Client()
        c.login(username="autor", password="autor")
        vote_response = c.post(
                "/api/votes/",
                data={ "publication":self.publication1.id,"vote":1},
                content_type='application/json',
            )
        self.assertEqual(vote_response.status_code, 201 ) 
        # повторная оценка публикации 

        vote_response = c.post(
                "/api/votes/",
                data={ "publication":self.publication1.id,"vote":1},
                content_type='application/json',
            )
        self.assertEqual(vote_response.status_code, 201 ) 
        content = vote_response.content

        assert content.find(b'"id":1,') > -1 


# эмулируем запросы для гостя
    def test_API_publications_listing_for_anonymous_user(self):
        """  список публикаций для гостя """ 
        c = Client()
        listing_response = c.get(
                "/api/publications/",
            )
        self.assertEqual(listing_response.status_code, 200 )


    def test_API_publications_adding_for_anonymous_user(self):
        """  добавления публикации - должно вызывать редирект на страницу логина """ 
        c = Client()
        add_response = c.post(
                "/api/publications/",
                data={ 'text':'Текст публикации 1' },
                headers={' Content-Type':'application/json' },
            )
        self.assertEqual(add_response.status_code, 403 )



    def test_API_publications_vote_for_anonymous_user(self):
        """  оценка публикации для залогиненного пользователя """ 
        c = Client()
        vote_response = c.post(
                "/api/votes/",
                data={ "publication":self.publication1.id,"vote":1},
                content_type='application/json',
            )
        self.assertEqual(vote_response.status_code, 403 ) 



from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import reverse


class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='user1')
        cls.post1 = Post.objects.create(
            title='post 1',
            text='this is post 1',
            status=Post.CHOICES[0][0],
            author=cls.user1,
        )
        cls.post2 = Post.objects.create(
            title='post 2',
            text='this is post 2',
            status=Post.CHOICES[1][0],
            author=cls.user1,
        )

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_details(self):
        self.assertEqual(self.post1.title, 'post 1')
        self.assertEqual(self.post1.text, 'this is post 1')

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_title(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)

    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_blog_page(self):
        response = self.client.get(reverse('post_details', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_status_404(self):
        response = self.client.get(reverse('post_details', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_show_draft_in_post_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'Some Title',
            'text': 'This is some text!',
            'status': 'pub',
            'author': self.user1.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Some Title')
        self.assertEqual(Post.objects.last().text, 'This is some text!')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'Post2 Updated',
            'text': 'this is text update',
            'status': 'pub',
            'author': self.post2.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Post2 Updated')
        self.assertEqual(Post.objects.last().text, 'this is text update')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)







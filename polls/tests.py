from django.test import TestCase
from django.urls import reverse
from .models import Question, Choice

class PollsViewTests(TestCase):
    
    def setUp(self):
        # Create a question for testing
        self.question = Question.objects.create(
            question_text='Sample Question?',
            pub_date='2023-10-20 00:00:00'
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text='Sample Choice',
            votes=0
        )
    
    def test_index_view(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')
        self.assertContains(response, 'Sample Question?')
    
    def test_detail_view(self):
        response = self.client.get(reverse('polls:detail', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/detail.html')
        self.assertContains(response, 'Sample Question?')
    
    def test_results_view(self):
        response = self.client.get(reverse('polls:results', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/results.html')
        self.assertContains(response, 'Sample Question?')


    def test_vote_view_with_valid_choice(self):
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice.id})
        self.assertRedirects(response, reverse('polls:results', args=(self.question.id,)))
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_vote_view_invalid_question(self):
        response = self.client.post(reverse('polls:vote', args=(999,)), {'choice': self.choice.id})
        self.assertEqual(response.status_code, 404)

import unittest
from math import ceil
from flaskr import create_app, db, Category, Question


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("flaskr/testing.py")
        self.client = self.app.test_client
        self.db = db

        if not Category.query.count() and not Question.query.count():
            from filldb import fill_database
            fill_database()

        # binds the app to the current context
        with self.app.app_context():
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def check_status_404(self, response):
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertTrue(not data.get("success_status"))
        self.assertEqual(data.get("message"), "The resource/s cannot be found")

    def check_status_422(self, response):
        data = response.get_json()
        self.assertEqual(response.status_code, 422)
        self.assertTrue(not data.get("success_status"))
        self.assertEqual(data.get("message"), "This operation cannot be done")

    def evaluate_questions_in_page(self, response, data, total_questions, qpp):
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data.get("questions")) <= qpp and len(data.get("questions")) != 0)
        self.assertEqual(data.get("total_questions"), total_questions)
        self.assertTrue(data.get("categories"))

    def step_0_get_all_categories(self):
        total_categories = Category.query.count()

        response = self.client().get("/categories")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data.get("categories")), total_categories)

    def step_1_get_category(self):
        category = Category.query.order_by(self.db.func.random()).first()
        category_id = category.id

        response = self.client().get(f"/categories/{category_id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("category"), category.format())

        response = self.client().get("/categories/fake-id")
        self.check_status_404(response)

    def step_2_get_questions_in_category(self):
        category = Category.query.order_by(self.db.func.random()).first()
        category_id = category.id
        total_questions = category.questions.count()
        for i in range(1, total_questions + 1):
            questions_per_page = i
            pages = ceil(total_questions / questions_per_page)

            for j in range(1, pages + 1):
                response = self.client().get(
                    f"/categories/{category_id}/questions",
                    query_string={
                        "page": j,
                        "length": i
                    }
                )
                data = response.get_json()
                self.evaluate_questions_in_page(response, data, total_questions, i)
                self.assertEqual(data.get("current_category").get("id"), category.id)
                self.assertEqual(data.get("current_category").get("type"), category.type)

        response = self.client().get("/categories/fake-id/questions")
        self.check_status_404(response)

    def step_3_get_all_questions(self):
        total_questions = Question.query.count()
        for i in range(1, total_questions + 1):
            questions_per_page = i
            pages = ceil(total_questions / questions_per_page)

            for j in range(1, pages + 1):
                response = self.client().get(
                    "/questions",
                    query_string={
                        "page": j,
                        "length": i
                    }
                )
                data = response.get_json()
                self.evaluate_questions_in_page(response, data, total_questions, i)
                self.assertTrue(not data.get("current_category"))

    def step_4_post_new_question(self):
        category_id = Category.query.order_by(self.db.func.random()).first().id

        question = {
            "question": "<from_test>",
            "answer": "<from_test>",
            "difficulty": 1,
            "category_id": category_id
        }

        response = self.client().post(
            "/questions",
            json=question
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get("success_status"))
        self.assertTrue(data.get("new_question").get("id"))
        self.assertEqual(data.get("new_question").get("question"), question.get("question"))
        self.assertEqual(data.get("new_question").get("answer"), question.get("answer"))
        self.assertEqual(data.get("new_question").get("difficulty"), question.get("difficulty"))
        self.assertEqual(data.get("new_question").get("category").get("id"), question.get("category_id"))
        self.assertEqual(data.get("message"), "addition operation has been done successfully")

        response = self.client().post(f"/questions")

        self.check_status_422(response)

    def step_5_post_search_questions(self):
        search = {
            "search_term": "<from_test>"
        }

        total_questions = Question.query.filter(Question.question.ilike(f"%{search.get('search_term')}%")).count()

        for i in range(1, total_questions + 1):
            questions_per_page = i
            pages = ceil(total_questions / questions_per_page)

            for j in range(1, pages + 1):
                response = self.client().post(
                    "/questions",
                    query_string={
                        "page": j,
                        "length": i
                    },
                    json=search
                )

                data = response.get_json()
                self.evaluate_questions_in_page(response, data, total_questions, i)
                self.assertTrue(not data.get("current_category"))

        response = self.client().post(
            "/questions",
            json={
                "search_term": "<not_found>"
            }
        )

        self.check_status_404(response)

    def step_6_get_question(self):
        question = Question.query.order_by(self.db.func.random()).first()
        question_id = question.id

        response = self.client().get(f"/questions/{question_id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("question"), question.format())

        response = self.client().get("/questions/fake-id")
        self.check_status_404(response)

    def step_7_delete_question(self):
        try:
            question = Question.query.filter(Question.question == "<from_test>").first()
            question_id = question.id

        except AttributeError:
            question = Question.query.order_by(self.db.func.random()).first()
            question_id = question.id

        response = self.client().delete(f"/questions/{question_id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get("success_status"))
        self.assertEqual(data.get("message"), "deletion operation has been done successfully")

        response = self.client().get("/questions/fake-id")
        self.check_status_404(response)

    def step_8_post_play_infinite_state(self):
        total_questions = 10
        previous_questions_ids = []

        for q_id in range(total_questions):
            response = self.client().post(
                "/quizzes",
                json={
                    "previous_questions_ids": previous_questions_ids
                }
            )

            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            previous_questions_ids.append(data.get("question").get("id"))

    def step_9_post_play_force_end_state(self):
        category = Category.query.order_by(self.db.func.random()).first()
        total_questions = category.questions.count()
        quiz_category_id = category.id
        previous_questions_ids = []

        for q_id in range(total_questions):
            response = self.client().post(
                "/quizzes",
                json={
                    "previous_questions_ids": previous_questions_ids,
                    "quiz_category_id": quiz_category_id
                }
            )

            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            try:
                self.assertTrue(data.get("question"))
                previous_questions_ids.append(data.get("question").get("id"))

            except AssertionError:
                break

        response = self.client().post("/quizzes")

        self.check_status_422(response)

    def _steps(self):
        for name in dir(self):
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        i = 1
        for name, step in self._steps():
            try:
                step()
                print(f"#{i}\t\t{name.replace('_', ' ')} <passed> ✔")

            except Exception as e:
                print(f"#{i}\t\t{name.replace('_', ' ')} <failed> ❌")
                self.fail(f"{name} failed ({type(e).__name__}: {e})")

            finally:
                i += 1


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

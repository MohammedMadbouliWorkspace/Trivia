from flask import Flask, request, json, jsonify, abort
from flask_cors import CORS
from ..models import db, migrate, Question, Category


def format_collection(collection):
    return [item.format() for item in collection]


def create_app(config_file):

    # Create and configure the app
    app = Flask(__name__)
    try:
        app.config.from_pyfile(config_file)

    except FileNotFoundError:
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI="postgres://trivia@localhost:5432/trivia",
            SQLALCHEMY_TRACK_MODIFICATIONS=True
        )

    db.init_app(app=app)
    migrate.init_app(app=app)

    # Set up CORS and allow '*' for origins
    cors = CORS(
        app=app,
        resources={
            r"/api/*": {"origins": "*"}
        }
    )

    # Concatenate Access-Control-Allow-<property> headers to any response
    @app.after_request
    def access_control(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    # ----------------------------------------------------------------------------#
    # Endpoints.
    # ----------------------------------------------------------------------------#

    #  All Categories.
    #  ----------------------------------------------------------------
    @app.route("/categories")
    def categories():
        """
        (1) Creates endpoint for fetching all categories
        (2) Methods: GET
        (3) Arguments: no arguments needed

        :return: JSON view for "categories" [collection]
        """

        return jsonify(
            {
                "categories": format_collection(
                    Category.query.all()
                )
            }
        )

    #  One Category.
    #  ----------------------------------------------------------------
    @app.route("/categories/<int:category_id>")
    def category(category_id):
        """
        (1) Creates endpoint for fetching specific category
        (2) Methods: GET
        (3) Arguments: no arguments needed

        :param category_id: To specify a category
        :return: JSON view for "category" [item]
        """

        try:
            return jsonify(
                {
                    "category": Category.query.get(category_id).format()
                }
            )

        except BaseException:
            abort(404)

    #  All Questions in a Category.
    #  ----------------------------------------------------------------
    @app.route("/categories/<int:category_id>/questions")
    def questions_in_category(category_id):
        """
        (1) Creates endpoint for fetching
            all questions paginated in specific category

        (2) Methods: GET

        (3) Arguments:
            - page=<integer: page_number> [optional, default=1]
            - length=<integer: items_per_page> [optional, default=10]

        :param category_id: To specify a category for its questions

        :return: JSON view for
                "questions" [collection],
                "total_questions" [item],
                "categories" [collection],
                "current_category" [item]
        """

        # Set questions per page value
        qpp = int(request.args.get("length", 10))

        # Set page number
        page = (int(request.args.get("page", 1)) - 1) * qpp

        try:

            # Fetch specific category by its id
            category = Category.query.get(category_id)

            return jsonify(
                {
                    "questions": format_collection(
                        category.questions.order_by(Question.id).offset(page).limit(qpp).all()
                    ),
                    "total_questions": category.questions.count(),
                    "categories": format_collection(
                        Category.query.all()
                    ),
                    "current_category": category.format()
                }
            )

        except BaseException:
            abort(404)

    #  All Questions.
    #  ----------------------------------------------------------------
    @app.route("/questions", methods=["GET", "POST"])
    def questions():
        """
        (1) Creates endpoint for:
            - fetching all questions paginated
            - Searching for questions by a keyword
            - Adding a new question

        (2) Methods: GET, POST

        (3) Arguments for GET, POST [in search state]:
            - page=<integer: page_number> [optional, default=1]
            - length=<integer: items_per_page> [optional, default=10]

        (4) Body for POST:

            - search for questions by providing:
                JSON Object {
                    "search_term": <string: search_keyword>
                }

            - or add new question by providing:
                JSON Object {
                    "question": <string: question>
                    "answer": <string: answer>
                    "difficulty": <integer: difficulty_number>
                    "category_id": <integer: category_id>
                }

        :return(GET): JSON view for
                    "questions" [collection],
                    "total_questions" [item],
                    "categories" [collection],
                    "current_category" [item]

        :return(POST):
            - in search state
                JSON view for
                "questions" [collection],
                "total_questions" [item],
                "categories" [collection],
                "current_category" [item]

            - in add state
                JSON view for
                "success_status" [boolean],
                "new_question" [item],
                "message" [string]

        """

        # Set questions per page value
        qpp = int(request.args.get("length", 10))

        # Set page number
        page = (int(request.args.get("page", 1)) - 1) * qpp

        if request.method == "GET":

            try:

                return jsonify(
                    {
                        "questions": format_collection(
                            Question.query.order_by(Question.id).offset(page).limit(qpp).all()
                        ),
                        "total_questions": Question.query.count(),
                        "categories": format_collection(
                            Category.query.all()
                        ),
                        "current_category": ""
                    }
                )

            except BaseException:
                abort(404)

        elif request.method == "POST":

            # Load json data from response body
            data = json.loads(request.data)

            # Get search term
            search_term = data.get("search_term")

            # Check if search term is provided
            if search_term:

                try:

                    # Fetch results
                    results = Question.query.filter(Question.question.ilike(f"%{search_term}%"))

                    # Format results for a single page
                    results_to_show = results.offset(page).limit(qpp).all()

                    return jsonify(
                        {
                            "questions": format_collection(
                                results_to_show
                            ),
                            "total_questions": len(results.all()),
                            "categories": format_collection(
                                Category.query.all()
                            ),
                            "current_category": ""
                        }
                    )

                except BaseException:
                    abort(404)

            else:
                try:

                    # Create a new Question instance
                    question = Question(
                        question=data.get("question"),
                        answer=data.get("answer"),
                        difficulty=data.get("difficulty"),
                        category_id=data.get("category_id")
                    )

                    # Commit add Question object
                    question.add()

                    return jsonify(
                        {
                            "success_status": True,
                            "new_question": question.format(),
                            "message": "addition operation has been done successfully"
                        }
                    )

                except BaseException:
                    db.session.rollback()
                    db.session.close()
                    abort(422)

    #  One Question.
    #  ----------------------------------------------------------------
    @app.route("/questions/<int:question_id>", methods=["GET", "DELETE"])
    def question(question_id):
        """
        (1) Creates endpoint for:
            - fetching specific question
            - deleting specific question

        (2) Methods: GET, DELETE

        (3) Arguments for GET, DELETE: no arguments needed

        :param question_id: To specify a question

        :return(GET): JSON view for "question" [item]

        :return(DELETE):
            JSON view for
            "success_status" [boolean],
            "message" [string]
        """

        try:

            # Fetch specific question by its id
            question = Question.query.get(question_id)

            if request.method == "GET":

                return jsonify(
                    {
                        "question": question.format()
                    }
                )

            elif request.method == "DELETE":

                try:

                    # Commit delete Question
                    question.delete()

                    return jsonify(
                        {
                            "success_status": True,
                            "message": "deletion operation has been done successfully"
                        }
                    )

                except BaseException:
                    abort(422)

        except BaseException:
            abort(404)

    #  Play Quizzes.
    #  ----------------------------------------------------------------
    @app.route("/quizzes", methods=["POST"])
    def quizzes():
        """
        (1) Creates endpoint:

            - For fetching random question in specific category (if provided)
            or in any category

            - And playing quizzes by providing a list of previous questions IDs
            to avoid repeating the same random questions

            - By continuing playing with specific category,
            if you reached the last question in this category,
            it'll make an end-game force by returning a false value within question

            - Most of the game implementation is dependent on the front end

        (2) Methods: POST

        (3) Arguments: no arguments needed

        (4) Body:
            JSON Object {
                "previous_questions_ids": <array>
                "quiz_category_id": <integer: category_id>
            }


        :return:
            - in infinite state
                JSON view for
                "question" [item]

            - in force-end state
                JSON view for
                "question" [boolean: false]
        """

        try:
            # Load json data from response body
            data = json.loads(request.data)

            # Get previous questions list of IDs
            previous_questions_ids = data.get("previous_questions_ids")

            # Get category id
            quiz_category_id = data.get("quiz_category_id")

            # Fetch specific category by its id
            # to be selected for game or select random category
            selected_category = Category.query.get(quiz_category_id) or Category.query.order_by(
                db.func.random()
            ).first()

            # Fetch a random question in the selected category for pre-playing
            random_question = selected_category.questions.order_by(db.func.random()).first()

            # Set force-end state to False
            force_end = False

            # Check for truth of provided category id to set force-end mechanism
            if quiz_category_id:

                # Set force-end mechanism
                force_end = selected_category.questions.count() == len(previous_questions_ids)

            # Avoid repeating the same question in the provided category
            while random_question.id in previous_questions_ids and not force_end:

                # Fetch a random question in the selected category
                random_question = selected_category.questions.order_by(db.func.random()).first()

            # Check for force-end state
            if force_end:

                return jsonify(
                    {
                        "question": False
                    }
                )

            return jsonify(
                {
                    "question": random_question.format()
                }
            )

        except BaseException:
            abort(422)

    # ----------------------------------------------------------------------------#
    # Error Handlers.
    # ----------------------------------------------------------------------------#

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success_status": False,
                "message": "The resource/s cannot be found"
            }
        ), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success_status": False,
                "message": "This operation cannot be done"
            }
        ), 422

    @app.errorhandler(405)
    def method_not_allowd(error):
        return jsonify(
            {
                "success_status": False,
                "message": "This method is not allowed in this endpoint"
            }
        ), 405

    return app

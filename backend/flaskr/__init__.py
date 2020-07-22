from flask import Flask, request, json, jsonify, abort
from flask_cors import CORS
from ..models import db, migrate, Question, Category


def format_collection(collection):
    return [item.format() for item in collection]


def create_app(config_file):
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

    cors = CORS(
        app=app,
        resources={
            r"/api/*": {"origins": "*"}
        }
    )

    @app.after_request
    def access_control(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    @app.route("/categories")
    def categories():
        return jsonify(
            {
                "categories": format_collection(
                    Category.query.all()
                )
            }
        )

    @app.route("/categories/<int:category_id>")
    def category(category_id):
        try:
            return jsonify(Category.query.get(category_id).format())

        except BaseException:
            abort(404)

    @app.route("/categories/<int:category_id>/questions")
    def questions_in_category(category_id):
        qpp = int(request.args.get("length", 10))
        page = (int(request.args.get("page", 1)) - 1) * qpp

        try:
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

    @app.route("/questions", methods=["GET", "POST"])
    def questions():
        qpp = int(request.args.get("length", 10))
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
            data = json.loads(request.data)
            search_term = data.get("search_term")
            if search_term:

                try:
                    results = Question.query.filter(Question.question.ilike(f"%{search_term}%"))
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
                    question = Question(
                        question=data.get("question"),
                        answer=data.get("answer"),
                        difficulty=data.get("difficulty"),
                        category_id=data.get("category")
                    )
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

    @app.route("/questions/<int:question_id>", methods=["GET", "DELETE"])
    def question(question_id):
        try:
            question = Question.query.get(question_id)
            if request.method == "GET":
                return jsonify(question.format())

            elif request.method == "DELETE":

                try:
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

    @app.route("/quizzes", methods=["POST"])
    def quizzes():
        try:
            data = json.loads(request.data)
            previous_questions_ids = data.get("previous_questions_ids")
            quiz_category_id = data.get("quiz_category_id")
            selected_category = Category.query.get(quiz_category_id) or Category.query.order_by(
                db.func.random()).first()
            random_question = selected_category.questions.order_by(db.func.random()).first()
            force_end = False

            if quiz_category_id:
                force_end = selected_category.questions.count() == len(previous_questions_ids)

            while random_question.id in previous_questions_ids and not force_end:
                random_question = selected_category.questions.order_by(db.func.random()).first()

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

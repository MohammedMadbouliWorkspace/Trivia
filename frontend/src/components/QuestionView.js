import React, {Component} from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
    constructor() {
        super();
        this.state = {
            questions: [],
            page: 1,
            totalQuestions: 0,
            categories: {},
            currentCategory: null,
        }
    }

    componentDidMount() {
        this.getQuestions();
    }

    getQuestions = () => {
        $.ajax({
            url: `/questions?page=${this.state.page}`,
            type: "GET",
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    categories: result.categories,
                    currentCategory: result.current_category
                })
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again')
            }
        })
    }

    selectPage(num, notUsed) {
        this.setState({page: num}, () => this.getQuestions());
    }

    selectCategoryPage(num, categoryId) {
        this.setState({page: num}, () => this.getByCategory(categoryId));
    }

    selectResultsPage(num, notUsed) {
        this.setState({page: num}, () => this.submitSearch(this.searchTerm));
    }

    selectPageMethod = this.selectPage

    searchTerm = ""

    fetchQuestionsMethod = this.getQuestions

    createPagination() {
        let pageNumbers = [];
        let maxPage = Math.ceil(this.state.totalQuestions / 10)
        for (let i = 1; i <= maxPage; i++) {
            pageNumbers.push(
                <span
                    key={i}
                    className={`page-num ${i === this.state.page ? 'active' : ''}`}
                    onClick={() => {
                        this.selectPageMethod(i, this.state.currentCategory.id)
                    }}>{i}
                </span>
            )
        }
        return pageNumbers.length === 1 ? "" : pageNumbers;
    }

    getByCategory = (id) => {
        $.ajax({
            url: `/categories/${id}/questions?page=${this.state.page}`,
            type: "GET",
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category
                })
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again')
            }
        })
    }

    defaultPage = (num) => {
        this.state.page = num
    }

    submitSearch = (searchTerm) => {
        $.ajax({
            url: `/questions?page=${this.state.page}`,
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({search_term: searchTerm}),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category
                })
                this.searchTerm = searchTerm
                this.selectPageMethod = this.selectResultsPage
                this.fetchQuestionsMethod = () => this.submitSearch(searchTerm)
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again')

            }
        })
    }

    questionAction = (id) => (action) => {
        if (action === 'DELETE') {
            if (window.confirm('are you sure you want to delete the question?')) {
                $.ajax({
                    url: `/questions/${id}`,
                    type: "DELETE",
                    success: (result) => {
                        this.fetchQuestionsMethod();
                    },
                    error: (error) => {
                        alert('Unable to load questions. Please try your request again')
                    }
                })
            }
        }
    }

    render() {
        return (
            <div className="question-view">
                <div className="categories-list">
                    <h2 onClick={() => {
                        this.state.page = 1
                        this.selectPageMethod = this.selectPage
                        this.fetchQuestionsMethod = this.getQuestions
                        this.getQuestions()
                    }}>Categories</h2>
                    <ul>
                        {Object.keys(this.state.categories).map((id,) => (
                            <li key={this.state.categories[id].id} onClick={() => {
                                this.state.page = 1
                                this.selectPageMethod = this.selectCategoryPage
                                this.fetchQuestionsMethod = () => this.getByCategory(this.state.categories[id].id)
                                this.getByCategory(this.state.categories[id].id)
                            }}>
                                {this.state.categories[id].type}
                                <img className="category" src={`${this.state.categories[id].type.toLowerCase()}.svg`}/>
                            </li>
                        ))}
                    </ul>
                    <Search submitSearch={this.submitSearch} defaultPage={this.defaultPage}/>
                </div>
                <div className="questions-list">
                    <h2>Questions</h2>
                    {this.state.questions.map((q, ind) => (
                        <Question
                            key={q.id}
                            question={q.question}
                            answer={q.answer}
                            category={q.category.type.toLowerCase()}
                            difficulty={q.difficulty}
                            questionAction={this.questionAction(q.id)}
                        />
                    ))}
                    <div className="pagination-menu">
                        {this.createPagination()}
                    </div>
                </div>

            </div>
        );
    }
}

export default QuestionView;

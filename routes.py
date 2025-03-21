from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Article

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@routes.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        users = User.query.all()
        return render_template('admin_dashboard.html', users=users)
    elif current_user.role == 'author':
        articles = Article.query.filter_by(author_id=current_user.id).all()
        return render_template('author_dashboard.html', articles=articles)
    elif current_user.role == 'reviewer':
        articles = Article.query.all()
        return render_template('reviewer_dashboard.html', articles=articles)
    return redirect(url_for('index'))

@routes.route('/submit_article', methods=['GET', 'POST'])
@login_required
def submit_article():
    if current_user.role != 'author':
        flash('Only authors can submit articles.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        article = Article(title=title, abstract=abstract, author_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        flash('Article submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('submit_article.html')

@routes.route('/review_article/<int:article_id>', methods=['POST'])
@login_required
def review_article(article_id):
    if current_user.role != 'reviewer':
        flash('Only reviewers can review articles.', 'danger')
        return redirect(url_for('dashboard'))
    
    article = Article.query.get_or_404(article_id)
    status = request.form['status']  # Approved or Rejected
    article.status = status
    db.session.commit()
    flash(f'Article {status} successfully!', 'success')
    return redirect(url_for('dashboard'))

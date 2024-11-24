from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms import TransactionForm
from datetime import datetime
import jinja2
import os
import matplotlib.pyplot as plt
import io
import base64

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# database Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    transactions = Transaction.query.all()

    # visualization: expenses by category
    categories = [t.category for t in transactions]
    amounts = [t.amount for t in transactions]
    plt.figure(figsize=(6, 4))
    plt.bar(categories, amounts)
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)

    # save plot to display in HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('dashboard.html', transactions=transactions, plot_url=plot_url)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        new_transaction = Transaction(
            category=form.category.data,
            amount=form.amount.data,
            description=form.description.data
        )
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_transaction.html', form=form)

if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)

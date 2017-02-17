from app import app
from flask import Flask, render_template, request, flash


@app.route('/', methods=['GET', 'POST'])
def main():
    """
    Stuff
    """
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Return login page
    """
    return render_template('login.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    Return search page
    """
    return render_template('search.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """
    Return edit page
    """
    return render_template('edit.html')

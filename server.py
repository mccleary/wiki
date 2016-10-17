from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, flash, render_template, request, redirect, session
import pg
import markdown

import wiki_linkify
from wiki_linkify import wiki_linkify
import os

app = Flask('Visit Tracker')
db = pg.DB(
    dbname=os.environ.get('PG_DBNAME'),
    host=os.environ.get('PG_HOST'),
    user=os.environ.get('PG_USERNAME'),
    passwd=os.environ.get('PG_PASSWORD')
)

## count number of times user is accessing site
# @app.route('/')
# def count():
#     count = session.get('count', 0)
#     session['count'] = count + 1
#     return '<h1>Current Count: %d</h1>' % session['count']
#

@app.route('/')
def hello():
    return render_template('layout.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    flash('%s, you have submitted your name!' % name)
    return redirect('/')


app.secret_key = 'hello happy kitty'

@app.route('/submit_login', methods=['POST'])
def submit_login():
    username = request.form.get('username')
    password = request.form.get('password')
    query = db.query("select * from users where username = $1", username)
    result_list = query.namedresult()
    print result_list

    if len(result_list) > 0:
        user = result_list[0]
        if user.password == password:
            # print "\n\n\nTESTING!!!\n\n\n"
            session['username'] = user.username
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return redirect('/login')




# @app.route('/<page_name>/edit')
# def edit_page(page_name):
#     if 'username' in session:
#         session['username'] = username
#         return redirect('/')
#     else:
#         return redirect('/login')
#
#
# @app.route('/logout')
# def logout():
#     del session['username']









@app.route('/')
def homepage():
        return redirect('/HomePage')

@app.route('/<page_name>')
def new_page_render(page_name):

    query = db.query('''
    select * from page
    where title = '%s' ''' % page_name).namedresult()
    print query
    print len(query)
    # print len(query[0])
    if len(query) == 0:
        return render_template(
            'placeholder.html',
            page_name=page_name)

    else:
        entry = query[0]
        entry_content = entry.page_content
        entry_content = wiki_linkify(entry_content)
        entry_content = markdown.markdown(entry_content)
        return render_template(
            'existing_page.html',
            entry=entry,
            page_name=page_name,
            entry_content=entry_content,)


@app.route('/<page_name>/edit')
def edit_page_render(page_name):
    # id = request.args.get('id')
    # if not id:
    #     return redirect('/')

    sql = "select * from page where title = '%s'" % page_name
    print sql
    result_list = db.query(sql).namedresult()
    if len(result_list) == 0:
        return render_template(
            'edit_page.html',
            page_name=page_name,)

    else:
        entry = result_list[0]
        return render_template(
        'edit_existing_page.html',
        page_name=page_name,
        entry=entry
    )


@app.route('/<page_name>/save', methods=['POST'])
def save_page(page_name):
    # title = request.form.get('title')
    page_content = request.form.get('edit')
    # last_modified_date = request.form.get('last_modified_date')
    # title = page_name,
    # page_content = wiki_linkify(page_content)
    # page_content = markdown.markdown(page_content)
    db.insert('page',
        title='%s' % page_name,
        page_content=page_content)
        # email=email)
    return redirect('/%s' %page_name)

@app.route('/<page_name>/update', methods=['POST'])
def submit_form(page_name):
    id = request.form.get('id')
    page_content = request.form.get('edit')
    # page_content = wiki_linkify(page_content)
    # page_content = markdown.markdown(page_content)
    db.update(
        'page',
        id=id,
        page_content=page_content)
    return redirect('/%s' %page_name)

@app.route('/AllPages')
def display_pages():
    allentries = db.query('select * from page')
    return render_template(
    'AllPages.html',
    page = allentries.namedresult()
    )

if __name__ == '__main__':
    app.run(debug=True)

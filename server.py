from flask import Flask, render_template, request, redirect
import pg
# import wiki_linkify

app = Flask('Wiki')
db = pg.DB(dbname='wiki_db')

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
        return render_template(
            'existing_page.html',
            entry=entry,
            page_name=page_name)


@app.route('/<page_name>/edit')
def edit_page_render(page_name):
    return render_template(
        'edit_page.html',
        page_name=page_name
    )


@app.route('/<page_name>/save', methods=['POST'])
def save_page(page_name):
    # title = request.form.get('title')
    page_content = request.form.get('edit')
    # last_modified_date = request.form.get('last_modified_date')
    # title = page_name,

    db.insert('page',
        title='%s' % page_name,
        page_content=page_content)
        # email=email)
    return redirect('/%s' %page_name)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'

db = SQLAlchemy(app)

class todo_list(db.Model):
	"""docstring for todo_list"""
	td_id = db.Column(db.Integer, primary_key=True)
	td_text = db.Column(db.String(200))
	#td_status = db.Column(db.Boolean)
	td_status = db.Column(db.String(60))
	posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route('/')
@app.route('/home')
@app.route('/index.html')
def index():
	todo_items_from_db = todo_list.query.order_by(todo_list.posted_on.desc()).filter_by(td_status='running').all()
	#todo_items_from_db = todo_list.query.oder_by(todo_list.posted_on.desc()).filter_by(td_status=False).all()
	done_items_from_db = todo_list.query.filter_by(td_status='completed').all()
	fail_items_from_db = todo_list.query.filter_by(td_status='failed').all()
	trash_items_from_db = todo_list.query.filter_by(td_status='trashed').all()
	#all_posts = BlogPost.query.order_by(BlogPost.posted_on.desc()).all()

	return render_template('index.html', todo_items_from_db=todo_items_from_db, done_items_from_db=done_items_from_db, trash_items_from_db=trash_items_from_db, fail_items_from_db=fail_items_from_db)


@app.route('/add', methods=['post'])
def add():
	todo_data = todo_list(td_text=request.form['todo_item'], td_status='running')
	db.session.add(todo_data)
	db.session.commit()
	return redirect(url_for('index'))
    #return '<h1>{}</h1>'.format(request.form['todo_item'])


# edit task ------------------------------------------------------------------------
@app.route('/edit/<td_id>', methods=['GET', 'POST'])
def edit(td_id):
	todo_data = todo_list.query.get_or_404(td_id)
	todo_items_from_db = todo_list.query.order_by(todo_list.posted_on.desc()).filter_by(td_status='running').all()
	done_items_from_db = todo_list.query.filter_by(td_status='completed').all()
	fail_items_from_db = todo_list.query.filter_by(td_status='failed').all()
	trash_items_from_db = todo_list.query.filter_by(td_status='trashed').all()

	if request.method == 'POST':
		todo_data.td_text = request.form['td_text']
		db.session.commit()
		return redirect('/')
	else:
		return render_template('edit.html', todo_data=todo_data, todo_items_from_db=todo_items_from_db, done_items_from_db=done_items_from_db, trash_items_from_db=trash_items_from_db, fail_items_from_db=fail_items_from_db)


@app.route('/completed/<td_id>')
def completed(td_id):
	todo_data = todo_list.query.filter_by(td_id=int(td_id)).first() #.first, since we're expecting one...
	todo_data.td_status = 'completed'
	db.session.commit()

	# print(request.form[1]) # let's us see what gets returned
	return redirect(url_for('index'))


@app.route('/undo_completed/<td_id>')
def undo_completed(td_id):
	todo_data = todo_list.query.filter_by(td_id=int(td_id)).first() #.first, since we're expecting one...
	todo_data.td_status = 'running'
	db.session.commit()

	# print(request.form[1]) # let's us see what gets returned
	return redirect(url_for('index'))


# TRASH -------------------------------
@app.route('/trash/<td_id>')
def trash(td_id):
	todo_data = todo_list.query.filter_by(td_id=int(td_id)).first() #.first, since we're expecting one...
	todo_data.td_status = 'trashed'
	db.session.commit()

	# print(request.form[1]) # let's us see what gets returned
	return redirect(url_for('index'))


# Restore -------------------------------
@app.route('/restore/<td_id>')
def restore(td_id):
	todo_data = todo_list.query.filter_by(td_id=int(td_id)).first() #.first, since we're expecting one...
	todo_data.td_status = 'running'
	db.session.commit()
	return redirect(url_for('index'))


# delete post -----------
@app.route('/delete/<td_id>')
def delete(td_id):
	todo_item = todo_list.query.get_or_404(td_id)
	db.session.delete(todo_item)
	db.session.commit()
	return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

    
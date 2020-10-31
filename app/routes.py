from app import app, db
from app.models import User, Notes
from app.forms import LoginForm, RegisterForm, CreateNoteForm, EditNoteForm, DeleteNoteForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CreateNoteForm()
    if form.validate_on_submit():
        note = Notes(owner_id=current_user.get_id(), title=form.note_name.data)
        db.session.add(note)
        db.session.commit()
        flash('Note created!')
    return render_template('index.html', title='Home', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Register complete, please login')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/notes', methods=['GET'])
def notes():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'new', type=str)

    if sort == 'new':
        notes = Notes.query.order_by(Notes.created_at.desc()).paginate(
            page, app.config['NOTES_PER_PAGE'], False)
    elif sort == 'old':
        notes = Notes.query.order_by(Notes.created_at.asc()).paginate(
            page, app.config['NOTES_PER_PAGE'], False)

    next_url = url_for('notes', page=notes.next_num) \
        if notes.has_next else None
    prev_url = url_for('notes', page=notes.prev_num) \
        if notes.has_prev else None

    return render_template('notes.html', title="Notes",
                           notes=notes.items, next_url=next_url, prev_url=prev_url,
                           request=request)


@app.route('/notes/<id>', methods=['GET', 'POST'])
def note(id):
    form = DeleteNoteForm()
    get_note = Notes.query.filter_by(owner_id=current_user.get_id(), id=id).first()
    if form.validate_on_submit():
        db.session.delete(get_note)
        db.session.commit()
        return redirect(url_for('notes'))
    return render_template('note.html', title="Note", note=get_note, form=form)


@app.route('/edit/notes/<id>', methods=['GET', 'POST'])
def edit_note(id):
    get_note = Notes.query.filter_by(owner_id=current_user.get_id(), id=id).first()

    html_due_date = str(get_note.due_date).split(' ')

    form = EditNoteForm()
    if form.validate_on_submit():
        get_note.title = form.title.data
        get_note.content = form.content.data
        get_note.due_date = form.due_date.data
        db.session.commit()
        return redirect(url_for('notes'))
    return render_template('edit_note.html', title="Edit", note=get_note, form=form, html_due_date=html_due_date[0])

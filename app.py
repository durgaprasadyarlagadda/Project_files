from flask import Flask, render_template, url_for, redirect , request , flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    branch = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000), nullable=False)
    option1 = db.Column(db.String(1000), nullable=False)
    option2 = db.Column(db.String(1000), nullable=False)
    option3 = db.Column(db.String(1000), nullable=False)
    option4 = db.Column(db.String(1000), nullable=False)
    correct_answer = db.Column(db.String(1000), nullable=False)
    exam_code = db.Column(db.String(1000), nullable=False)

class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(30), nullable=False)
    exam_code = db.Column(db.String(1000), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    

class ExamForm(FlaskForm):
    question = StringField(validators=[InputRequired()], render_kw={"placeholder": "Question"})
    option1 = StringField(validators=[InputRequired()], render_kw={"placeholder": "Option 1"})
    option2 = StringField(validators=[InputRequired()], render_kw={"placeholder": "Option 2"})
    option3 = StringField(validators=[InputRequired()], render_kw={"placeholder": "Option 3"})
    option4 = StringField(validators=[InputRequired()], render_kw={"placeholder": "Option 4"})
    correct_answer = StringField(validators=[InputRequired()], render_kw={"placeholder": "Correct Answer"})

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    full_name = StringField(validators=[
                           InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Full Name"})
    mobile_number = StringField(validators=[
                           InputRequired(), Length(min=10, max=15)], render_kw={"placeholder": "Mobile Number"})
    branch = StringField(validators=[
                           InputRequired(), Length(min=1, max=30)], render_kw={"placeholder": "Branch"})
    role = SelectField('Role', choices=[('student', 'Student'), ('admin', 'Admin')])
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.role == 'admin':
                    return redirect(url_for('admin_page'))
                elif user.role == 'student':
                    return redirect(url_for('student_page'))
    return render_template('login.html', form=form)


@app.route('/admin_page', methods=['GET', 'POST'])
@login_required
def admin_page():
    return render_template('admin_page.html')

@app.route('/student_page', methods=['GET', 'POST'])
@login_required
def student_page():
    return render_template('student_page.html',current_user=current_user)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',current_user=current_user)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, full_name=form.full_name.data, mobile_number = form.mobile_number.data,branch = form.branch.data,role = form.role.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/create_exam', methods=['GET', 'POST'])
@login_required
def create_exam():
    form = ExamForm()
    if request.method == 'POST':
        exam_code = request.form.get('exam_code')
        num_questions = int(request.form.get('num_questions'))

        for i in range(1, num_questions + 1):
            question = request.form.get(f'question-{i}')
            option1 = request.form.get(f'option1-{i}')
            option2 = request.form.get(f'option2-{i}')
            option3 = request.form.get(f'option3-{i}')
            option4 = request.form.get(f'option4-{i}')
            correct_answer = request.form.get(f'correct_answer-{i}')

            new_question = Exam(
                question=question,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_answer=correct_answer,
                exam_code=exam_code
            )

            db.session.add(new_question)

        db.session.commit()
        return redirect(url_for('admin_page'))

    return render_template('create_exam.html', form=form)

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        exam_code = request.form.get('exam_code')
        exam = Exam.query.filter_by(exam_code=exam_code).all()

        if not exam:
            flash('Exam code does not exist.', 'error')
            return redirect(url_for('quiz'))

        marks = Marks.query.filter_by(username=current_user.username, exam_code=exam_code).first()
        if marks:
            flash('You have already attempted this exam.', 'error')
            return redirect(url_for('quiz'))

        return render_template('take_quiz.html', exam=exam, exam_code=exam_code)

    return render_template('quiz.html', current_user=current_user)


@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    exam_code = request.form.get('exam_code')
    exam = Exam.query.filter_by(exam_code=exam_code).all()

    if not exam:
        flash('Exam code does not exist.', 'error')
        return redirect(url_for('quiz'))

    marks = Marks.query.filter_by(username=current_user.username, exam_code=exam_code).first()
    if marks:
        flash('You have already attempted this exam.', 'error')
        return redirect(url_for('quiz'))

    total_marks = 0
    for question in exam:
        question_id = question.id
        correct_answer = question.correct_answer
        chosen_answer = request.form.get(f'answer-{question_id}')

        if chosen_answer == correct_answer:
            total_marks += 1

    new_marks = Marks(
        username=current_user.username,
        full_name=current_user.full_name,
        branch=current_user.branch,
        exam_code=exam_code,
        marks=total_marks
    )
    db.session.add(new_marks)
    db.session.commit()

    flash('Quiz submitted successfully!', 'success')
    return redirect(url_for('quiz'))


@app.route('/take_quiz', methods=['POST'])
@login_required
def take_quiz():
    exam_code = request.form.get('exam_code')
    exam = Exam.query.filter_by(exam_code=exam_code).all()

    if not exam:
        flash('Exam code does not exist.', 'error')
        return redirect(url_for('quiz'))

    marks = Marks.query.filter_by(username=current_user.username, exam_code=exam_code).first()
    if marks:
        flash('You have already attempted this exam.', 'error')
        return redirect(url_for('quiz'))

    return render_template('take_quiz.html', exam=exam, exam_code=exam_code)

@app.route('/student_details')
@login_required
def student_details():
    students = User.query.filter_by(role='student').all()
    return render_template('student_details.html', students=students)

@app.route('/marks_details')
@login_required
def marks_details():
    marks = Marks.query.all()
    if not marks:
        message = 'No one has submitted Quiz yet.'
        return render_template('marks.html', message=message)

    return render_template('marks.html', marks=marks)


if __name__ == "__main__":
    app.run(debug=True)

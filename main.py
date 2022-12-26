from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_bootstrap import Bootstrap
from forms import ProfileForm, CompleteForm, Account, FoP, Contact, RegisterForm, LoginForm, Comment_FoP, Vision_FoP, Comment_Vision, Vision_Details, Goals, Task_Item
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SEC_KEY")
# app.config['SECRET_KEY'] = '8BYkEfBA606donzWlSihBXox7C0sKR6b'
Bootstrap(app)
ckeditor = CKEditor()
ckeditor.init_app(app)

# FILE_URL = 'sqlite:///C:/Users/kappesser/PycharmProjects/data/sam19.db'
FILE_URL = 'sqlite:///sam36.db'
COMPANY_ID = 'company.com'

# connect to db
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", FILE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1", FILE_URL)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# class MySQLAlchemy(SQLAlchemy):
#     Column: Callable
#     String: Callable
#     Integer: Callable
#     Text: Callable
#     ForeignKey: Callable
#
# db = MySQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))


class Association(db.Model):
    __tablename__ ="association_table"
    member_id = db.Column(db.ForeignKey("team.id"), primary_key=True)
    fop_id = db.Column(db.ForeignKey("fop.id"), primary_key=True)
    role = db.Column(db.String(20), nullable=False)

    current_fop = relationship("Field_Of_Play", back_populates="associated_members")
    assigned_member = relationship("Member", back_populates="associated_fops")


class Member(UserMixin, db.Model):
    __tablename__ ="team"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    comment_fop = relationship("Comment_FOP", back_populates="fop_author")
    comment_vision = relationship("Comments_Vision", back_populates="comment_author")
    # assigned_fops = relationship('Field_Of_Play', secondary=fop_team, back_populates='assigned_members')
    associated_fops = relationship("Association", back_populates="assigned_member")


class Overall_Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    account_img = db.Column(db.String(250), nullable=False)
    branch = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    fops = relationship("Field_Of_Play", back_populates="large_account")

class Field_Of_Play(db.Model):
    __tablename__ = "fop"
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    # large_account = relationship("Overall_Account", back_populates="fops")
    large_account = relationship("Overall_Account", back_populates="fops")
    contacts = relationship("Buying_Center", back_populates="dedicated_fop")
    comments = relationship("Comment_FOP", back_populates="fop_to_comment" )
    vision = relationship("Vision_FOP", back_populates="fop_vision")

    fop_name = db.Column(db.String(250), unique=True, nullable=False)
    fop_description = db.Column(db.Text, nullable=False)
    fop_business = db.Column(db.Text, nullable=False)
    value_add = db.Column(db.Text, nullable=False)
    customer_perception = db.Column(db.Text, nullable=False)
    # assigned_members = relationship("Member", secondary=fop_team, back_populates="assigned_fops")
    associated_members = relationship("Association", back_populates="current_fop")

class Buying_Center(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    fop_id = db.Column(db.Integer, db.ForeignKey("fop.id"))
    dedicated_fop = relationship("Field_Of_Play", back_populates="contacts")

    contact_name = db.Column(db.String(250), unique=True, nullable=False)
    contact_role = db.Column(db.String(250), nullable=False)
    contact_relation = db.Column(db.Integer(), nullable=False)
    contact_significance = db.Column(db.Integer(), nullable=False)

class Comment_FOP(db.Model):
    __tablename__ = "comment_fop"
    id = db.Column(db.Integer, primary_key=True)
    fop_id = db.Column(db.Integer, db.ForeignKey("fop.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    fop_comment = db.Column(db.Text, nullable=False)
    fop_to_comment = relationship("Field_Of_Play", back_populates="comments")
    fop_author = relationship("Member", back_populates="comment_fop")

class Vision_FOP(db.Model):
    __tablename__ = "vision_fop"
    id = db.Column(db.Integer, primary_key=True)
    fop_id = db.Column(db.Integer, db.ForeignKey("fop.id"))
    status_today = db.Column(db.Text, nullable=False)
    charter_statement = db.Column(db.Text, nullable=False)
    fop_vision = relationship("Field_Of_Play", back_populates="vision")
    comments = relationship("Comments_Vision", back_populates="vision_to_comment")
    details = relationship("Detailed_Vision", back_populates="vision_of_details")

class Comments_Vision(db.Model):
    __tablename__ = "comment_vision"
    id = db.Column(db.Integer, primary_key=True)
    vision_id = db.Column(db.Integer, db.ForeignKey("vision_fop.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    vision_comment = db.Column(db.Text, nullable=False)
    vision_to_comment = relationship("Vision_FOP", back_populates="comments")
    comment_author = relationship("Member", back_populates="comment_vision")

class Detailed_Vision(db.Model):
    __tablename__ = "vision_details"
    id = db.Column(db.Integer, primary_key=True)
    vision_id = db.Column(db.Integer, db.ForeignKey("vision_fop.id"))

    stakeholder_relation = db.Column(db.Text, nullable=False)
    business_context = db.Column(db.Text, nullable=False)
    value_add = db.Column(db.Text, nullable=False)
    customer_perception = db.Column(db.Text, nullable=False)
    vision_of_details = relationship("Vision_FOP", back_populates="details")
    goals = relationship("Related_Goals", back_populates="related_detailed_vision")


class Related_Goals(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    detailed_vision_id = db.Column(db.Integer, db.ForeignKey("vision_details.id"))
    goal_title = db.Column(db.Text, nullable=False)
    goal_description = db.Column(db.Text, nullable=False)
    related_vision_detail = db.Column(db.Text, nullable=False)
    goal_reached = db.Column(db.Integer, nullable=False)
    related_detailed_vision = relationship("Detailed_Vision", back_populates="goals")
    tasks = relationship("Tasks", back_populates="related_goal")

class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))
    task_title = db.Column(db.Text, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    task_owner = db.Column(db.Text, nullable=False)
    task_status = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Text, nullable=False)
    related_goal = relationship("Related_Goals", back_populates="tasks")

db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if COMPANY_ID in form.email.data:

            plain_password = form.password.data
            hashed_password = generate_password_hash(plain_password, method='pbkdf2:sha256', salt_length=8)

            new_member = Member(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=hashed_password
            )
            db.session.add(new_member)
            db.session.commit()
        else:
            return render_template('access_denied.html')
        return redirect(url_for('start'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_email = form.email.data
        login_member = Member.query.filter_by(email=login_email).first()
        if not login_member:
            flash("User doesn't exist! Give in existing email address")
            return render_template("login.html")

        login_password = form.password.data
        saved_password = login_member.password

        if check_password_hash(saved_password, login_password):
            login_user(login_member)
            return redirect(url_for('start'))
        else:
            flash('your password is not correct, try again')
            return render_template('login')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('start'))

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/accounts')
@login_required
def accounts():
    all_accounts = Overall_Account.query.all()
    return render_template('list_accounts.html', accounts=all_accounts, current_user=current_user)


@app.route('/new_account', methods=['GET', 'POST'])
def add_new_account():
    form = Account(
        body="This is a Description of main Activities and Business Goals of the Account"
    )
    if form.validate_on_submit():
        new_account = Overall_Account(
            name=form.account_name.data,
            branch=form.branch.data,
            account_img=form.img_url.data,
            description=form.body.data
        )
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('accounts'))
    return render_template('add_account.html', form=form)


@app.route('/account/<int:account_id>', methods=['GET', 'POST'])
def show_account(account_id):
    requested_account = Overall_Account.query.get(account_id)
    return render_template('show_account.html', account=requested_account)

@app.route('/edit_account/<int:account_id>', methods=['GET', 'POST'])
def edit_account(account_id):
    current_account = Overall_Account.query.get(account_id)
    form = Account(
        account_name=current_account.name,
        branch=current_account.branch,
        img_url=current_account.account_img,
        body=current_account.description
    )
    if form.validate_on_submit():
        current_account.name = form.account_name.data
        current_account.branch = form.branch.data
        current_account.account_img = form.img_url.data
        current_account.description = form.body.data
        print(current_account.account_img)
        db.session.commit()
        return redirect(url_for("show_account", account_id=current_account.id))
    return render_template('add_account.html', form=form, is_edit=True, account=current_account)


@app.route('/fop_list/<int:account_id>')
def show_fop_list(account_id):
    current_account = Overall_Account.query.get(account_id)
    fop_list = Field_Of_Play.query.filter_by(account_id=account_id).all()
    return render_template('list_fop.html', account=current_account, fop_list=fop_list)

@app.route('/add_fop/<int:account_id>', methods=['GET', 'POST'])
def add_fop(account_id):
    current_account = Overall_Account.query.get(account_id)
    form = FoP()
    if form.validate_on_submit():
        new_fop = Field_Of_Play(
            fop_name=form.fop_name.data,
            fop_description=form.fop_description.data,
            fop_business=form.fop_business.data,
            value_add=form.our_contribution.data,
            customer_perception=form.customer_perception.data,
            large_account=current_account
        )
        db.session.add(new_fop)
        db.session.commit()
        return redirect(url_for('show_fop_list', account_id=account_id))

    return render_template('add_fop.html', form=form, account=current_account)

@app.route('/fop/<int:fop_id>', methods=['GET', 'POST'])
def show_fop(fop_id):
    form = Comment_FoP()
    requested_fop = Field_Of_Play.query.get(fop_id)
    all_comments = Comment_FOP.query.filter_by(fop_to_comment=requested_fop).all()
    if form.validate_on_submit():
        comment = Comment_FOP(
            fop_comment=form.comment.data,
            fop_to_comment=requested_fop,
            fop_author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('show_fop', fop_id=fop_id))

    return render_template('show_fop.html', form=form, fop=requested_fop, all_comments=all_comments)

@app.route('/edit_fop/<int:fop_id>', methods=['GET', 'POST'])
def edit_fop(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    print(current_fop.fop_name)
    print(current_fop.large_account.name)
    form = FoP(
        fop_name=current_fop.fop_name,
        fop_description=current_fop.fop_description,
        fop_business=current_fop.fop_business,
        our_contribution=current_fop.value_add,
        customer_perception=current_fop.customer_perception
    )

    if form.validate_on_submit():
        current_fop.fop_name = form.fop_name.data
        current_fop.fop_description = form.fop_description.data
        current_fop.fop_business = form.fop_business.data
        current_fop.value_add = form.our_contribution.data
        current_fop.customer_perception = form.customer_perception.data
        db.session.commit()
        return redirect(url_for('show_fop', fop_id=fop_id))

    return render_template('add_fop.html', form=form, is_edit=True, fop=current_fop, account=current_fop.large_account)

@app.route('/show-buying-center/<int:fop_id>', methods=['GET', 'POST'])
def show_buying_center(fop_id):
    contacts = Buying_Center.query.filter_by(fop_id=fop_id).all()
    current_fop = Field_Of_Play.query.get(fop_id)
    print(current_fop.fop_name)
    return render_template('show_buying_center.html', fop=current_fop, contacts=contacts)

@app.route('/add-contact/<int:fop_id>', methods=['GET', 'POST'])
def add_contact(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    form = Contact()
    if form.validate_on_submit():
        new_contact = Buying_Center(
            contact_name=form.contact_name.data,
            contact_role=form.contact_role.data,
            contact_relation=form.contact_relation.data,
            contact_significance=form.contact_significance.data,
            dedicated_fop=current_fop
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('show_buying_center', fop_id=fop_id))
    return render_template('add_contact.html', form=form, fop_id=fop_id)

@app.route('/edit-contact/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    current_contact = Buying_Center.query.get(contact_id)
    form = Contact(
        contact_name=current_contact.contact_name,
        contact_role=current_contact.contact_role,
        contact_relation=current_contact.contact_relation,
        contact_significance=current_contact.contact_significance,
    )
    if form.validate_on_submit():
        current_contact.contact_name = form.contact_name.data
        current_contact.contact_role = form.contact_role.data
        current_contact.contact_relation = form.contact_relation.data
        current_contact.contact_significance = form.contact_significance.data

        db.session.commit()
        return redirect(url_for('show_buying_center', fop_id=current_contact.dedicated_fop.id))

    return render_template('add_contact.html', form=form, contact_id=contact_id, is_edit=True)

@app.route('/fop_team/<int:fop_id>', methods=['GET', 'POST'])
def show_fop_team(fop_id):
    fop = Field_Of_Play.query.get(fop_id)
    all_fop_associations = Association.query.filter_by(current_fop=fop).all()
    fop_team = [member.assigned_member for member in all_fop_associations]

    return render_template("show_fop_team.html", fop_team=fop_team, all_fop_associations=all_fop_associations, fop_id=fop_id)

@app.route('/assign_members/<int:fop_id>', methods=['GET', 'POST'])
def assign_members(fop_id):
    all_members = Member.query.all()
    fop = Field_Of_Play.query.get(fop_id)
    all_fop_associations = Association.query.filter_by(current_fop=fop).all()
    fop_team = [member.assigned_member for member in all_fop_associations]

    if request.method == 'POST':
            assigned_member_ids = request.form.getlist('check')
            assigned_member_list = [Member.query.get(id) for id in assigned_member_ids]

            assigned_roles = request.form.getlist('select')
            id_list = []
            index = 0

            for member in all_members:
                if member in assigned_member_list:
                    id_list.append(all_members.index(member))

            for member in assigned_member_list:
                if member not in fop_team:
                    role = assigned_roles[id_list[index]]
                    associations = Association(
                        role=role,
                        assigned_member=member,
                        current_fop=fop
                    )
                    db.session.add(associations)
                    db.session.commit()
                index = index + 1

            for member in fop_team:
                if member not in assigned_member_list:
                    association_to_delete = Association.query.filter_by(assigned_member=member).first()
                    db.session.delete(association_to_delete)
                    db.session.commit()

            return redirect(url_for('show_fop_team', fop_id=fop_id))

    return render_template("assign_members.html", all_members=all_members, fop_id=fop_id, fop_team=fop_team )

@app.route('/check_account_manager')
def check_acm():
    fop_name = request.args.get('a', 0, type=str)
    current_fop = Field_Of_Play.query.filter_by(fop_name=fop_name).first()
    all_fop_associations = Association.query.filter_by(current_fop=current_fop).all()
    fop_team = [member.assigned_member for member in all_fop_associations]
    print(fop_team)
    if current_user not in fop_team:
        result = False
    else:
            wright_association = Association.query.filter_by(current_fop=current_fop, assigned_member=current_user).first()
            if wright_association.role == "Account Manager":
                result = True
            else:
                result = False
    return jsonify(result=result)

@app.route('/show_vision/<int:fop_id>', methods=['GET', 'POST'])
def show_vision(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    vision = Vision_FOP.query.filter_by(fop_vision=current_fop).first()
    vision_details = Detailed_Vision.query.filter_by(vision_of_details=vision).first()
    all_comments = Comments_Vision.query.filter_by(vision_to_comment=vision).all()
    all_contacts = Buying_Center.query.filter_by(dedicated_fop=current_fop)
    form = Comment_Vision()
    if vision == None:
        return redirect(url_for('add_vision', fop_id=fop_id))

    if form.validate_on_submit():
        comment = Comments_Vision(
            vision_comment=form.comment.data,
            vision_to_comment=vision,
            comment_author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('show_vision', fop_id=fop_id))

    return render_template('show_vision.html', vision=vision, vision_details=vision_details, fop_id=fop_id, current_fop=current_fop, all_comments=all_comments, all_contacts=all_contacts, form=form)


@app.route('/add_vision/<int:fop_id>', methods=['GET', 'POST'])
def add_vision(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    form = Vision_FoP()
    if form.validate_on_submit():
        new_vision = Vision_FOP(
            status_today=form.current_situation.data,
            charter_statement=form.charter_statement.data,
            fop_vision=current_fop
        )
        db.session.add(new_vision)
        db.session.commit()
        return redirect(url_for('show_vision', fop_id=fop_id))

    return render_template('add_vision.html', form=form, fop_id=fop_id, is_edit=False)

@app.route('/edit_vision/<int:fop_id>', methods=['GET', 'POST'])
def edit_vision(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    vision = Vision_FOP.query.filter_by(fop_vision=current_fop).first()
    form = Vision_FoP(
        current_situation=vision.status_today,
        charter_statement=vision.charter_statement
    )
    if form.validate_on_submit():
        vision.status_today = form.current_situation.data
        vision.charter_statement = form.charter_statement.data
        db.session.commit()
        return redirect(url_for('show_vision', fop_id=fop_id))

    return render_template("add_vision.html", fop_id=fop_id,  form=form, is_edit=True)

@app.route('/add_vision_details/<int:fop_id>', methods=['GET', 'POST'])
def add_vision_details(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    vision = Vision_FOP.query.filter_by(fop_vision=current_fop).first()
    form = Vision_Details()

    if form.validate_on_submit():
        vision_details = Detailed_Vision(
            stakeholder_relation=form.stakeholder_relation.data,
            business_context=form.business_context.data,
            value_add=form.value_add.data,
            customer_perception=form.customer_perception.data,
            vision_of_details=vision
        )
        db.session.add(vision_details)
        db.session.commit()
        return redirect(url_for('show_vision', fop_id=fop_id))

    return render_template('add_vision.html', form=form, fop_id=fop_id, is_edit=False)


@app.route('/edit_vision_details/<int:fop_id>', methods=['GET', 'POST'])
def edit_vision_details(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    vision = Vision_FOP.query.filter_by(fop_vision=current_fop).first()
    vision_details = Detailed_Vision.query.filter_by(vision_of_details=vision).first()
    form = Vision_Details(
        stakeholder_relation=vision_details.stakeholder_relation,
        business_context=vision_details.business_context,
        value_add=vision_details.value_add,
        customer_perception=vision_details.customer_perception
    )
    if form.validate_on_submit():
        vision_details.stakeholder_relation = form.stakeholder_relation.data
        vision_details.business_context = form.business_context.data
        vision_details.value_add = form.value_add.data
        vision_details.customer_perception = form.customer_perception.data
        db.session.commit()
        return redirect(url_for('show_vision', fop_id=fop_id))


    return render_template("add_vision_details.html", form=form, fop_id=fop_id, is_edit=True)

@app.route("/strategy/<int:fop_id>", methods=["GET", "POST"])
def strategy(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    vision = Vision_FOP.query.filter_by(fop_vision=current_fop).first()
    vision_details = Detailed_Vision.query.filter_by(vision_of_details=vision).first()
    all_goals = Related_Goals.query.filter_by(related_detailed_vision=vision_details).all()
    form = Goals()

    if form.validate_on_submit():
        print("stage2")
        new_goal = Related_Goals(
        goal_title=form.goal_title.data,
        goal_description=form.goal_description.data,
        goal_reached=0,
        related_vision_detail=form.related_vision_topic.data,
        related_detailed_vision=vision_details
        )
        db.session.add(new_goal)
        db.session.commit()
        return redirect(url_for('strategy', fop_id=fop_id))


    return render_template("show_strategy.html", current_fop=current_fop, vision=vision, vision_details=vision_details, fop_id=fop_id, form=form, all_goals=all_goals)


@app.route("/add_tasks/<int:goal_id>/<int:fop_id>", methods=["GET", "POST"])
def add_tasks(goal_id, fop_id):
    # current_fop = Field_Of_Play.query.get(fop_id)
    # vision = Vision_FOP.query.filter_by(fop_vision=current_fop).first()
    # vision_details = Detailed_Vision.query.filter_by(vision_of_details=vision).first()
    current_goal = Related_Goals.query.get(goal_id)
    form = Task_Item(
        due_date="  sth. like: March 2023, or 25.05.2023 "
    )
    if form.validate_on_submit():
        new_task = Tasks(
            task_title=form.task_title.data,
            task_description=form.task_description.data,
            task_owner=form.task_owner.data,
            due_date=form.due_date.data,
            task_status="open",
            related_goal=current_goal
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('strategy', fop_id=fop_id))
    return render_template("add_task.html", form=form, current_goal=current_goal, is_edit=False)



@app.route("/show_tasks/<int:fop_id>", methods=["GET", "POST"])
def show_tasks(fop_id):
    current_fop = Field_Of_Play.query.get(fop_id)
    vision = Vision_FOP.query.filter_by(fop_vision=current_fop).first()
    vision_details = Detailed_Vision.query.filter_by(vision_of_details=vision).first()
    all_goals = Related_Goals.query.filter_by(related_detailed_vision=vision_details).all()

    all_tasks_lists = []
    for goal in all_goals:
        tasks_per_goal = Tasks.query.filter_by(related_goal=goal).all()
        all_tasks_lists.append(tasks_per_goal)
    all_tasks = sum(all_tasks_lists, [])
    print(f"length of all_tasks: {len(all_tasks)}")

    if request.method == 'POST':
        assigned_status_list = request.form.getlist('select')
        print(assigned_status_list)

        for i in range(0, len(all_tasks)):
            all_tasks[i].task_status = assigned_status_list[i]
            print(all_tasks[i].task_status)
            db.session.commit()




    return render_template("show_tasks.html", all_tasks=all_tasks, current_fop=current_fop, fop_id=fop_id)




if __name__ == '__main__':
    app.run(debug=True)

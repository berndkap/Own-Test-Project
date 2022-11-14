from flask import Flask, render_template, url_for, request, redirect, flash
from flask_bootstrap import Bootstrap
from forms import ProfileForm, CompleteForm, Account, FoP, Contact, RegisterForm, LoginForm
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)
ckeditor = CKEditor()
ckeditor.init_app(app)

# FILE_URL = 'sqlite:///C:/Users/kappesser/PycharmProjects/data/sam19.db'
FILE_URL = 'sqlite:///sam.db'
COMPANY_ID = 'company.com'

# connect to db
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", FILE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = FILE_URL
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

fop_team = db.Table('fop_team',
                    db.Column('member_id', db.Integer, db.ForeignKey('team.id')),
                    db.Column('fop_id', db.Integer, db.ForeignKey('fop.id'))
)


class Member(UserMixin, db.Model):
    __tablename__ ="team"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    assigned_fops = relationship('Field_Of_Play', secondary=fop_team, back_populates='assigned_members')


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

    fop_name = db.Column(db.String(250), unique=True, nullable=False)
    fop_description = db.Column(db.Text, nullable=False)
    fop_business = db.Column(db.Text, nullable=False)
    value_add = db.Column(db.Text, nullable=False)
    customer_perception = db.Column(db.Text, nullable=False)
    assigned_members = relationship("Member", secondary=fop_team, back_populates="assigned_fops")

class Buying_Center(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    fop_id = db.Column(db.Integer, db.ForeignKey("fop.id"))
    dedicated_fop = relationship("Field_Of_Play", back_populates="contacts")

    contact_name = db.Column(db.String(250), unique=True, nullable=False)
    contact_role = db.Column(db.String(250), nullable=False)
    contact_relation = db.Column(db.Integer(), nullable=False)
    contact_significance = db.Column(db.Integer(), nullable=False)


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
    # all_members = db.session.query(Member).all()

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

# @app.route('/new-account', methods=['GET', 'POST'])
# def new_account():
#
#     if request.method == 'POST':
#         data = request.form.get
#         account = request.form['account_name']
#         branch = request.form['branch_name']
#         number = request.form['number']
#         select = request.form['selected_name']
#         value = request.form.getlist('check')
#         value2 = request.form.getlist('check2')
#         radio_value = request.form.getlist('flexRadioDefault')
#         switch1 = request.form.getlist('switch1')
#         print(account)
#         print(branch)
#         print(number)
#         print(select)
#         print(value)
#         print(value2)
#         print(radio_value)
#         print(switch1)
#
#         return redirect(url_for('start'))
#
#     return render_template('new-account.html')

# @app.route('/wtforms_layout', methods=['GET', 'POST'])
# def wtf_layout():
#     print("soweit gekommen")
#     form = ProfileForm()
#     print("noch weiter")
#     if form.validate_on_submit():
#         print(form.account_name.data)
#         print(form.main_contact.data)
#         print(form.email.data)
#         # print(form.birthday.data)
#         # print(form.level.data)
#         return redirect(url_for('start'))
#     return render_template('wtf_flask_forms.html', form=form)

# @app.route('/wtf2', methods=['GET', 'POST'])
# def wtf2():
#     form = ProfileForm()
#     form.body.data = "This is a Description of main Activities and Business Goals of the Account"
#     if form.validate_on_submit():
#         print('Hello')
#         print(form.account_name.data)
#         print(form.main_contact.data)
#         print(form.email.data)
#         print(form.role.data)
#         print(form.range.data)
#         print(form.multiple_file.data)
#         print(form.body.data)
#         return redirect(url_for('start'))
#
#     return render_template('wtf2.html', form=form)

# @app.route('/layout')
# def layout_new_account():
#     return render_template('layout-new-account.html')

# @app.route('/wtf3', methods=['GET', 'POST'])
# def wtf3():
#     form = ProfileForm()
#     return render_template(('wtf3.html'))

# start real implementation here!

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
    print("yes!!")
    current_account = Overall_Account.query.get(account_id)
    fop_list = Field_Of_Play.query.filter_by(account_id=account_id).all()
    # print(fop_list)
    # print(fop_list[2].id)
    return render_template('list_fop.html', account=current_account, fop_list=fop_list)

@app.route('/add_fop/<int:account_id>', methods=['GET', 'POST'])
def add_fop(account_id):
    print("success")
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

@app.route('/fop/<int:fop_id>')
def show_fop(fop_id):
    print("angekommen")
    requested_fop = Field_Of_Play.query.get(fop_id)
    print(requested_fop)
    print(fop_id)
    return render_template('show_fop.html', fop=requested_fop)

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
        customer_perception=current_fop.customer_perception,
        # large_account=current_fop.large_account
    )
    if form.validate_on_submit():
        current_fop.fop_name = form.fop_name.data
        current_fop.fop_description = form.fop_description.data
        current_fop.fop_business = form.fop_business.data
        current_fop.value_add = form.our_contribution.data
        current_fop.customer_perception = form.customer_perception.data
        # large_account=current_account
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
    fop_team = fop.assigned_members
    return render_template("show_fop_team.html", fop_team=fop_team, fop_id=fop_id)

@app.route('/assign_members/<int:fop_id>', methods=['GET', 'POST'])
def assign_members(fop_id):
    all_members = Member.query.all()
    fop = Field_Of_Play.query.get(fop_id)
    fop_team = fop.assigned_members

    if request.method == 'POST':
            assigned_member_ids = request.form.getlist('check')
            assigned_member_list = [Member.query.get(id) for id in assigned_member_ids]

            for member in assigned_member_list:
                if member not in fop_team:
                    fop.assigned_members.append(member)
            for member in fop_team:
                if member not in assigned_member_list:
                    fop.assigned_members.remove(member)
            db.session.commit()
            return redirect(url_for('show_fop_team', fop_id=fop_id))

    return render_template("assign_members.html", all_members=all_members, fop_id=fop_id, fop_team=fop_team )

if __name__ == '__main__':
    app.run(debug=True)

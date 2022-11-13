from wtforms import PasswordField, StringField, validators, DateTimeField, IntegerField, SubmitField, IntegerRangeField, EmailField, SelectField, BooleanField, MultipleFileField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class ProfileForm(FlaskForm):
    account_name = StringField(label='Account Name', validators=[DataRequired()])
    main_contact = StringField(label='Main Contact', validators=[DataRequired()])
    role = SelectField(label='Role in Buying center', choices=['Decision Maker', 'Influencer', 'Our Coach'])
    email = EmailField(label='Email Address', validators=[DataRequired()])
    range = IntegerRangeField(label='How good do you know this contact')
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
    multiple_file = MultipleFileField('multiple fies test')
    body = CKEditorField('Account Description')
    submit = SubmitField('Submit')



# extend class easily
class CompleteForm(ProfileForm):
    birthday = DateTimeField('Birthday', format='%m/%d/%y')
    level = IntegerField('Hierarchy Level', [validators.NumberRange(min=0, max=5)])
    account_name2 = StringField('Account Name', [validators.Length(min=4, max=25)])
    submit = SubmitField('Submit')

class Account(FlaskForm):
    account_name = StringField(label='Account Name', validators=[DataRequired()])
    branch = SelectField(label='Branch', choices=['Retail', 'Energy', 'Automotive', 'Other Industries'])
    body = CKEditorField('Account Descriptions')
    img_url = StringField("Account Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')

class FoP(FlaskForm):
    fop_name = StringField(label='FoP Name', validators=[DataRequired()])
    fop_description = CKEditorField('FoP Descriptions')
    fop_business = CKEditorField('FoP Business')
    our_contribution = CKEditorField('Our Value Add')
    customer_perception = CKEditorField('Customer Perception')
    submit = SubmitField('Submit')

class Contact(FlaskForm):
    contact_name = StringField(label='Contact Name', validators=[DataRequired()])
    # contact_role = StringField(label='Contact Role', validators=[DataRequired()])
    contact_role = SelectField(label='Role in Buying center', choices=['Decision Maker', 'Influencer', 'Our Coach', 'Sponsor', 'Anti-Sponsor', 'Procurement', 'Technical Support'])
    # contact_relation = IntegerField('Contact Relation', [validators.NumberRange(min=0, max=10)])
    contact_relation = IntegerRangeField(label='How good is our relation with this contact')
    # contact_significance = IntegerField('Contact Significance', [validators.NumberRange(min=0, max=10)])
    contact_significance = IntegerRangeField(label='How import is this contact regarding to our business')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    email = EmailField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = EmailField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
class Member(UserMixin, db.Model):
    __tablename__ ="team"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Overall_Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    account_img = db.Column(db.String(250), nullable=False)
    branch = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # fops = relationship("Field_OF_Play", back_populates="large_account")

class Field_Of_Play(db.Model):
    __tablename__ = "fop"
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    # large_account = relationship("Overall_Account", back_populates="fops")
    large_account = relationship("Overall_Account", backref="fops")

    fop_name = db.Column(db.String(250), unique=True, nullable=False)
    fop_description = db.Column(db.Text, nullable=False)
    fop_business = db.Column(db.Text, nullable=False)
    value_add = db.Column(db.Text, nullable=False)
    customer_perception = db.Column(db.Text, nullable=False)

class Buying_Center(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    fop_id = db.Column(db.Integer, db.ForeignKey("fop.id"))
    dedicated_fop = relationship("Field_Of_Play", backref="contacts")

    contact_name = db.Column(db.String(250), unique=True, nullable=False)
    contact_role = db.Column(db.String(250), nullable=False)
    contact_relation = db.Column(db.Integer(), nullable=False)
    contact_significance = db.Column(db.Integer(), nullable=False)

# db.create_all()

#!/usr/bin/env python
#coding:utf-8
"""
	account.py
	~~~~~~~~~~~~~
	:license: BSD, see LICENSE for more details.
"""


from flask import request, flash, jsonify, g, current_app,\
	abort, redirect, url_for, session, Blueprint
from application.helpers import render_template
from application.models import User

account=Blueprint('account',__name__,template_folder="../templates")

@account.route("/login/", methods=("GET","POST"))
def login():
    
    form = LoginForm(login=request.args.get('login',None),
                     next=request.args.get('next',None))

    if form.validate_on_submit():

        user, authenticated = User.query.authenticate(form.login.data,
                                                      form.password.data)

        if user and authenticated:
            session.permanent = form.remember.data
            
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            flash(_("Welcome back, %(name)s", name=user.username), "success")

            next_url = form.next.data

            if not next_url or next_url == request.path:
                next_url = url_for('frontend.people', username=user.username)

            return redirect(next_url)

        else:
            flash(_("Sorry, invalid login"), "error")

    return render_template("account/login.html", form=form)

    
@account.route("/signup/", methods=("GET","POST"))
def signup():
    
    form = SignupForm(next=request.args.get('next',None))

    if form.validate_on_submit():

        code = UserCode.query.filter_by(code=form.code.data).first()

        if code:
            user = User(role=code.role)
            form.populate_obj(user)

            db.session.add(user)
            db.session.delete(code)
            db.session.commit()

            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            flash(_("Welcome, %(name)s", name=user.nickname), "success")

            next_url = form.next.data

            if not next_url or next_url == request.path:
                next_url = url_for('frontend.people', username=user.username)

            return redirect(next_url)
        else:
            form.code.errors.append(_("Code is not allowed"))

    return render_template("account/signup.html", form=form)

    
@account.route("/logout/")
def logout():

    flash(_("You are now logged out"), "success")
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    next_url = request.args.get('next','')

    if not next_url or next_url == request.path:
        next_url = url_for("frontend.index")

    return redirect(next_url)

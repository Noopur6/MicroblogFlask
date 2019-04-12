'''
Created on Apr 12, 2019

@author: nsno
'''
from flask import render_template
from app import microblogapp, db

@microblogapp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@microblogapp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
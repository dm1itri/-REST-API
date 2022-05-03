from flask import Flask, render_template, redirect, request, abort, Blueprint, jsonify

from data.jobs import Job
from data.users import User
from data import db_session


api = Blueprint('api', __name__, url_prefix='/api')


@api.get('/jobs')
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created.name'))
                 for item in jobs]
        }
    )
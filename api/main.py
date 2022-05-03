from flask import Flask, render_template, redirect, request, abort, Blueprint, jsonify, make_response

from data.jobs import Job
from data.users import User
from data import db_session


api = Blueprint('api', __name__, url_prefix='/api')


@api.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.get('/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created.name'))
                 for item in jobs]
        }
    )


@api.get('/job/<int:id>')
def get_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == id).first()
    if job:
        return jsonify(
            {'job': job.to_dict(only=('title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created.name'))}
        )
    return jsonify({'job': f'Job with id={id} not found'})


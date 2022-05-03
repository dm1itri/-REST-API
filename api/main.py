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
                [item.to_dict(only=('id', 'title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created.name'))
                 for item in jobs]
        }
    )


@api.get('/jobs/<int:id>')
def get_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == id).first()
    if job:
        return jsonify(
            {f'job {id}': job.to_dict(only=('title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created.name'))}
        )
    return jsonify({'job': f'Job with id={id} not found'})


@api.post('/jobs')
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(Job).filter(Job.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    job = Job(
        id=request.json['id'],
        title=request.json['title'],
        team_leader_id=request.json['team_leader_id'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        user_created=request.json['user_created']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})



import json
import datetime
from flask import request
from sqlalchemy import and_

from . import apiendpoint
from ..models import db, ApiKey, Stat
from myvyosapp import app

@apiendpoint.route('/api/updateTrack', methods=['POST'])
def updateTrackTrack():
    postdata=request.form
    if request.form is not None:
        system_id = postdata.get("system_id");
        track = postdata.get("track_id")
        if (system_id is not None and track is not None):
            stat = Stat.query.filter_by(system_id=system_id).first()
            stat.track = track;
            db.session.add(stat)
            db.session.commit()

        else:
            return json.dumps({'status':'failed'})

    else:
        return json.dumps({'status':'failed'})


    return json.dumps({'status':'updated'})

@apiendpoint.route('/api', methods=['POST'])
def api():
    postdata = request.json
    if postdata is not None:
        if postdata.get('api_key') is not None:
            apiObj = ApiKey.query.filter_by(apikey=postdata.get('api_key')).first()
            if apiObj is not None:
                stats = postdata.get("stats")
                if stats is not None:
                    stat = Stat.query.filter(and_(Stat.user_id==apiObj.user_id, Stat.system_id==stats.get('system_id'))).first()
                    ip = request.headers.getlist("CF-Connecting-IP")[0]
                    ## Sanitize the IP for testing
                    ip = "XXXX:XXXX:XXXX::XX"
                    if stat is None:
                        stat = Stat(
                            user_id=apiObj.user_id,
                            system_id=stats.get('system_id'),
                            cpu=stats.get('cpu_percent'),
                            mem=stats.get('mem_percent'),
                            root_usage=stats.get('root_usage'),
                            version=stats.get('version'),
                            uptime=stats.get('uptime'),
                            hostname=stats.get('hostname'),
                            last_update=datetime.datetime.now(),
                            remote_addr=ip,
                            track='crux'
                            )
                    else:
                        stat.user_id=apiObj.user_id,
                        stat.system_id=stats.get('system_id'),
                        stat.cpu=stats.get('cpu_percent'),
                        stat.mem=stats.get('mem_percent'),
                        stat.root_usage=stats.get('root_usage'),
                        stat.version=stats.get('version'),
                        stat.uptime=stats.get('uptime'),
                        stat.hostname=stats.get('hostname'),
                        stat.last_update=datetime.datetime.now(),
                        stat.remote_addr=ip


                    db.session.add(stat)
                    db.session.commit()

                else:
                    return json.dumps({'status':'InvalidStatsPosted'})

            else:
                return json.dumps({'status':'APIKeyNotFound'})

        else:
            return json.dumps({'status':'InvalidApiKey'})

    return json.dumps({'status':'OK'})

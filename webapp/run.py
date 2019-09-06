#!/usr/bin/env python
from myvyosapp import app
from myvyosapp import config
from myvyosapp.models import db, Track


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        if Track.query.filter_by(track='crux').first() is None:
            crux = Track(track='crux', current_version='1.2.2', version_url='http://cdn.vyos.io/1.2.2.18247/vyos-1.2.2-amd64.iso')
            db.session.add(crux)
            db.session.commit()

        if Track.query.filter_by(track='crux_EPA').first() is None:
            crux_epa = Track(track='crux_EPA', current_version='1.2.3-epa1', version_url='http://cdn.vyos.io/1.2.3-epa1.38573/vyos-1.2.3-epa1-amd64.iso')
            db.session.add(crux_epa)
            db.session.commit()

    app.run(host="0.0.0.0", debug=app.config['DEBUG'])

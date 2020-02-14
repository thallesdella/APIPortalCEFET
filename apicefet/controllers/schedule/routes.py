from apicefet.controllers.schedule import Schedule

schedule = Schedule()
schedule.blueprint.add_url_rule('', 'time', schedule.horarios)

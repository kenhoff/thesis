def main(c):
	from datetime import datetime

	exec_string = '''SELECT gameid, acceptTime, submitTime from results'''
	c.execute(exec_string)
	deltas = []
	for row in c.fetchall():
		acceptTime = datetime.strptime(row[1], '%a %b %d %H:%M:%S PST %Y')
		submitTime = datetime.strptime(row[2], '%a %b %d %H:%M:%S PST %Y')
		# date_obj = datetime.strptime(row[1], '%c')

		deltas.append(((submitTime - acceptTime).total_seconds(), row[0]))

	print deltas

	count = 0
	sum = 0
	for delta in deltas:
		sum += delta[0]
		count += 1

	print("Average of all times: {} minutes".format((sum/count) / 60))

	games = ['oregon','lightbot','darfur','munchers', 'machine', 'pandemic', 'botlogic', 'baseball', 'notpron', 'lemmings']

	for game in games:
		count = 0
		sum = 0
		for delta in deltas:
			if (delta[1] == game):
				sum += delta[0]
				count += 1

		print("Average of {1} times: {0} minutes".format(((sum/count) / 60), game))



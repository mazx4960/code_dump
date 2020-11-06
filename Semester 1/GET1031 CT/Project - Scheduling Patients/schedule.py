patients = {
	"A": [2, True, 1200],
	"B": [2, False, 1215],
	"C": [1, False, 1215],
	"D": [1, True, 1245],
	"E": [2, True, 1245],
	"F": [1, False, 1300],
	"G": [2, False, 1315],
	"H": [1, True, 1315],
	"I": [1, False, 1330],
	"J": [1, True, 1345],
	"K": [2, False, 1345],
	"L": [2, True, 1415],
	"M": [1, False, 1430],
	"N": [1, False, 1445],
	"O": [2, True, 1515],
	"P": [2, False, 1515],
	"Q": [1, True, 1545],
	"R": [1, False, 1600],
	"S": [2, True, 1630],
	"T": [2, False, 1645],
}

doctors = {
	1: [1300, 1330],
	2: [1200, 1215, 1230, 1245, 1300, 1315, 1330, 1345],
	3: [1315, 1345, 1400, 1415, 1430, 1445],
	4: [1400, 1415, 1430, 1445, 1500, 1515, 1530, 1545],
	5: [1500, 1515, 1530, 1545, 1600, 1615, 1630, 1645]
}

output = {}

timeslots = [
	1200, 1215, 1230, 1245,
	1300, 1315, 1330, 1345,
	1400, 1415, 1430, 1445,
	1500, 1515, 1530, 1545,
	1600, 1615, 1630, 1645,
	1700
]

for timeslot in timeslots:
	possible_patients = sorted([p for p in patients if patients[p][2] == timeslot], key=lambda p: patients[p][0], reverse=True)
	possible_doctors = [d for d in doctors if timeslot in doctors[d]]
	specialised_p = [p for p in possible_patients if patients[p][1]]
	specialised_d = [d for d in possible_doctors if d == 2 or d == 5]

	print('=====================')
	print(timeslot)
	print(possible_patients, possible_doctors, specialised_p, specialised_d)

	cur_patient = -1
	while possible_doctors != [] and possible_patients != []:
		if specialised_p != []:
			cur_patient = specialised_p[0]
		else:
			cur_patient = possible_patients[0]

		if specialised_p != []:
			if specialised_d != []:
				cur_doc = specialised_d[0]
				output[cur_patient] = [timeslot, cur_doc]
				possible_patients.remove(cur_patient)
				specialised_p.remove(cur_patient)
				doctors[cur_doc].remove(timeslot)
				possible_doctors.remove(cur_doc)

				for p in possible_patients:
					patients[p][0] += 1
					patients[p][2] = timeslots[timeslots.index(timeslot) + 1]
				del patients[cur_patient]
			else:
				patients[cur_patient][0] += 1
				patients[cur_patient][2] = timeslots[timeslots.index(timeslot) + 1]
				possible_patients.remove(cur_patient)
				specialised_p = []
		else:
			cur_doc = possible_doctors[0]
			output[cur_patient] = [timeslot, cur_doc]
			doctors[cur_doc].remove(timeslot)
			possible_doctors.remove(cur_doc)
			possible_patients.remove(cur_patient)
			for p in possible_patients:
				patients[p][0] += 1
				patients[p][2] = timeslots[timeslots.index(timeslot) + 1]
			del patients[cur_patient]

	print()
	print(output)
	print()

print(output)
# print(patients)
# print(doctors)




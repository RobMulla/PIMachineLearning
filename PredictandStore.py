from Code import modelactions as ma 

predict_points = []

# Open predict_points.csv
with open('predict_points.csv', 'r') as f:
  reader = f.readlines()
  predict_points_raw = list(reader)

# Strip newline commands
for i in predict_points_raw:
	predict_points.append(i.rstrip('\n'))

# Predict and store
ma.predict_and_store(predict_points)
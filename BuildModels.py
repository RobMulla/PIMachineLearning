# Build Models

## LIST THE POINTS FOR THE MODEL TO BUILD IN A
## FILE CALLED build_points.csv

from Code import modelactions as ma 

build_points = []

# Open predict_points.csv
with open('build_points.csv', 'r') as f:
  reader = f.readlines()
  build_points_raw = list(reader)

# Strip newline commands
for i in build_points_raw:
	build_points.append(i.rstrip('\n'))


# Predict and store
ma.build_and_save_models(build_points)
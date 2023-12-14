#!/bin/sh

if [ ! -d /grade ]; then
  echo "ERROR: /grade not found! Mounting may have failed."
  exit 1
fi

# the autograder directory
AG_DIR='/grader'

# the parent directory containing everything about this grading job
export JOB_DIR='/grade'
# the job subdirectories
STUDENT_DIR=$JOB_DIR'/student'
TEST_DIR=$JOB_DIR'/tests'
OUT_DIR=$JOB_DIR'/results'

# where we will copy everything
export MERGE_DIR=$JOB_DIR'/run'

# now set up the stuff so that our run.sh can work
mkdir $MERGE_DIR
mkdir $OUT_DIR

mv $STUDENT_DIR/* $MERGE_DIR
mv $AG_DIR/* $MERGE_DIR
mv $TEST_DIR/* $MERGE_DIR

# user does not need a copy of this script
rm -f "$MERGE_DIR/run.sh"

echo "[run] starting autograder"

# run grader
cd $MERGE_DIR
python3 matlab_execute.py

# if that didn't work, then print a last-ditch message
if [ ! -s $OUT_DIR/results.json ]
then
  echo '{"succeeded": false, "score": 0.0, "message": "Your code could not be processed by the autograder. Please contact course staff and have them check the logs for this submission."}' > $OUT_DIR/results.json
fi

echo "[run] autograder finished"
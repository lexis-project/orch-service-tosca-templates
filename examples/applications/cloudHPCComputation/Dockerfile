# Dockerfile of a docker image used as LEXIS Template default pre-processing
# and post-processing container image.
# It just list files in $INPUT_DIR (default: /input_dataset)
# and stores the ouput in a result file (default: /output/results.txt)
#
FROM busybox

ENV INPUT_DIR ${INPUT_DIR:-"/input_dataset"}
ENV RESULT_DIR ${RESULT_DIR:-"/output/"}
ENV RESULT_FILE_NAME ${RESULT_FILE_PATH:-"results.txt"}
CMD mkdir -p $RESULT_DIR && ls -lR $INPUT_DIR | tee $RESULT_DIR/$RESULT_FILE_NAME


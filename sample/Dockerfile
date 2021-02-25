FROM busybox

ENV INPUT_DIR ${INPUT_DIR:-"/input_dataset"}
ENV RESULT_DIR ${RESULT_DIR:-"/output/"}
ENV RESULT_FILE_NAME ${RESULT_FILE_PATH:-"results.txt"}
CMD mkdir -p $RESULT_DIR && ls -lrt $INPUT_DIR | tee $RESULT_DIR/$RESULT_FILE_NAME


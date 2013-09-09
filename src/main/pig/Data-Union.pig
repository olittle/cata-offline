
RMF $OUTPUT/JYMBII-batch/final-score
data = load '$OUTPUT/JYMBII-batch/TMP/final-score-tmp' USING BinaryJSON();
org = load '$OUTPUT/JYMBII-batch/TMP/orginal-score' USING BinaryJSON();
data = union data, org; 
 
store data into '$OUTPUT/JYMBII-batch/final-score' USING BinaryJSON('intent','algorithmId','sourceId');

---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Seniority.pig
--
-- Purpose :
--
-- Creation Date : 24-07-2013
--
-- Last Modified : Sun 04 Aug 2013 01:53:52 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.


%declare kernel   `uname -s`
%default now      `date "+%s"`
%default daysago  1
%declare tzoffset `bash -c 'if [[ "$kernel" == "Linux" ]]; then echo "-28800";  else echo "0"; fi'`
%declare tzero    `echo $(($now - 60 * 60 * 24 * $daysago + $tzoffset))`

%declare REPORT_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y/%m/%d"; else date -r $tzero "+%Y/%m/%d"; fi'`
%declare e `echo $REPORT_DATE`

post_feast = LOAD '/data/derived/liar/grandfathering/members_postFeast/#LATEST' USING BinaryJSON(); 
post_feast = FOREACH post_feast GENERATE (int) id AS memberId, FLATTEN(fields); 
post_feast = FOREACH post_feast GENERATE memberId, fields::name AS f_name, fields::termVector AS termVector; 

seniority = FILTER post_feast BY f_name == 'maxJobSeniorityV2'; 
seniority = FOREACH seniority GENERATE (int)memberId AS memberId, FLATTEN(termVector); 
data = FOREACH seniority GENERATE memberId, (int)termVector::id AS score; 

member = load '$OUTPUT/JYMBII-batch/TMP/MemList' USING BinaryJSON(); 
member = foreach member generate (int) memberId as memberId;

senior = join data by memberId, member by memberId using 'replicated';
senior = distinct senior parallel 1; 
senior = foreach senior generate 's' as label, data::memberId as memberId, data::score as score; 
store senior into '$OUTPUT/JYMBII-batch/TMP/Member-Senior-Score/' USING BinaryJSON('memberId'); 

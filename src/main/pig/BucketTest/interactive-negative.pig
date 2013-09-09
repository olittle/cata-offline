---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : interactive-negative.pig
--
-- Purpose :
--
-- Creation Date : 19-07-2013
--
-- Last Modified : Wed 07 Aug 2013 02:09:06 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

register './impr_no_click.py' using jython as myfuncs;

%declare kernel   `uname -s`
%default now      `date "+%s"`
%default daysago  1
%declare tzoffset `bash -c 'if [[ "$kernel" == "Linux" ]]; then echo "-28800";  else echo "0"; fi'`
%declare tzero    `echo $(($now - 60 * 60 * 24 * $daysago + $tzoffset))`

%declare REPORT_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y/%m/%d"; else date -r $tzero "+%Y/%m/%d"; fi'`
%declare e `echo $REPORT_DATE`


%declare dzero    `echo $(($now - 60 * 60 * 24 * 40 + $tzoffset))`
%declare DELETE_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$dzero" "+%Y%m%d"; else date -r $dzero "+%Y%m%d"; fi'`
%declare y `echo $DELETE_DATE`

RMF $OUTPUT/JYMBII-batch/history/impression-inter-neg/$REPORT_DATE
RMF $OUTPUT/JYMBII-batch/history/impression-inter-neg/$DELETE_DATE

impr = LOAD '$OUTPUT/JYMBII-batch/history/impression/$REPORT_DATE' USING BinaryJSON();
view = LOAD '$OUTPUT/JYMBII-batch/history/view/$REPORT_DATE' USING BinaryJSON();
impr = foreach impr generate memberId, time, jobId;
view = foreach view generate memberId, time, jobId;

non_view = cogroup impr by memberId inner, view by memberId inner; 
non_view = foreach non_view generate group as memberId, myfuncs.NonView(impr, view) as negs; 

non_view = filter non_view by not IsEmpty(negs); 
non_view = foreach non_view generate memberId, FLATTEN(negs);
non_view = foreach non_view generate memberId, negs::jobId as jobId; 
non_view = distinct non_view parallel 1;
 
store non_view into '$OUTPUT/JYMBII-batch/history/impression-inter-neg/$REPORT_DATE' USING BinaryJSON('memberId'); 

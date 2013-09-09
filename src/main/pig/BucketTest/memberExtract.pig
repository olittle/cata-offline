---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : memberExtract.pig
--
-- Purpose : Extract the member
--
-- Creation Date : 19-07-2013
--
-- Last Modified : Wed 07 Aug 2013 02:17:18 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com)
-- Updated By : Haishan Liu
--_._._._._._._._._._._._._._._._._._._._._.


--Read off member list from JYMBII recs directly.
--The diff between the list of two consecutive days consists of new members.
--For new members, they don't have historical data anyways, so the
--previously snapshotted history can remain intact with regard to the diff.
data = load '/data/derived/liar/jymbii/jymbii-batch/recs/#LATEST' USING BinaryJSON();
data = filter data by sourceId == 18041;
member = foreach data generate sourceId as memberId;

rmf $OUTPUT/JYMBII-batch/MemberList
store memberinto '$OUTPUT/JYMBII-batch/MemberList' USING BinaryJSON('memberId');

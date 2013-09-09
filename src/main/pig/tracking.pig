---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : tracking.pig
--
-- Purpose :
--
-- Creation Date : 29-06-2013
--
-- Last Modified : Sat 29 Jun 2013 12:58:54 AM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

data = LOAD '/data/tracking/ProfileViewEvent/' USING LiAvroStorage('date.range','start.date=20130620;end.date=20130628;error.on.missing=false');
data1 = foreach data generate entityView.viewerId as viewerId, entityView.targetId as vieweeId;
data1 = filter data1 by vieweeId == 183180431;

dump data1;

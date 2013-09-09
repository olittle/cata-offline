---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Job-PostFeast.pig
--
-- Purpose :
--
-- Creation Date : 24-07-2013
--
-- Last Modified : Wed 24 Jul 2013 09:20:33 AM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

data = load '$OUTPUT/JYMBII/TrainingData/SeniorityData/' as (memberId:int, score:int); 

member = load '$OUTPUT/JYMBII/LinkedIn/MemberList/' USING BinaryJSON(); 
member = foreach member generate (int) memberId as memberId;

senior = join data by memberId, member by memberId parallel 100; 

store senior into '$OUTPUT/JYMBII/LinkedIn/MemberSeniorityScore';  

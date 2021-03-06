"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

import collections
import update
#from batch_farm_monitor.models import UserData, JobData, TimeData
from batch_farm_monitor.farms.farm_abstract import UserData, JobData, TimeData

class SimpleTest(TestCase):
	def test_update_fetch_data_bad_addr(self):
		remote = "ssh -o 'BatchMode yes' badaddress"

		fs_obj, farm_obj = update.import_modules(remote, None, "slurm")
		co1, co2, errno1, errno2 = update.fetch_data(fs_obj, farm_obj)

		self.assertEqual(errno1, 255)
		self.assertEqual(errno2, 255)
		self.assertEqual(co1, '')
		self.assertEqual(co2, '')

	def test_update_fetch_data_bad_cmd(self):
		remote = "sssh -o 'BatchMode yes' localhost"

		fs_obj, farm_obj = update.import_modules(remote, None, "slurm")
		co1, co2, errno1, errno2 = update.fetch_data(fs_obj, farm_obj)

		self.assertEqual(errno1, 127)
		self.assertEqual(errno2, 127)
		self.assertEqual(co1, '')
		self.assertEqual(co2, '')

	def test_update_fetch_data_fail_batch_mode(self):
		remote = "ssh -o 'BatchMode yes' localhost"

		fs_obj, farm_obj = update.import_modules(remote, None, "slurm")
		co1, co2, errno1, errno2 = update.fetch_data(fs_obj, farm_obj)

		self.assertEqual(errno1, 255)
		self.assertEqual(errno2, 255)
		self.assertEqual(co1, None)
		self.assertEqual(co2, None)

	def test_update_fetch_data_fail_batch_mode(self):
		remote = "ssh -o 'BatchMode yes' unknows@localhost"

		fs_obj, farm_obj = update.import_modules(remote, None, "slurm")
		co1, co2, errno1, errno2 = update.fetch_data(fs_obj, farm_obj)

		self.assertEqual(errno1, 255)
		self.assertEqual(errno2, 255)
		self.assertNotEqual(co1, None)
		self.assertNotEqual(co2, None)
		self.assertEqual(errno1 == 255 and co1 is not None, True)
		self.assertEqual(errno2 == 255 and co2 is not None, True)

	def test_update_parse_qstat_for_jobs(self):
		return
		jobs1 = ("\n\n"
			"Job ID               Username Queue    Jobname    SessID NDS   TSK Memory Time  S Time\n"
			"-------------------- -------- -------- ---------- ------ ----- --- ------ ----- - -----\n"
			"6248064.cronos.e12.p rmuenzer farmqe   param_hf_u  15179     1  --   30mb 02:00 R 00:27   dallas/0\n"
			"6248065.cronos.e12.p rmuenzer farmqe   param_hf_u  16133     1  --   30mb 02:00 R 00:23   dallas/1\n"
			"6248066.cronos.e12.p rmuenzer farmqe   param_hf_u  15656     1  --   30mb 02:00 R 00:24   dallas/2\n"
			"6248067.cronos.e12.p rmuenzer farmqe   param_hf_u  16565     1  --   30mb 02:00 R 00:23   dallas/3\n"
			"6248068.cronos.e12.p rmuenzer farmqe   param_hf_u  16995     1  --   30mb 02:00 R 00:22   dallas/4\n"
			"6248069.cronos.e12.p rmuenzer farmqe   param_hf_u  17467     1  --   30mb 02:00 R 00:20   dallas/5\n"
			"6248070.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248071.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248072.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248073.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248074.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248075.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248076.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248077.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248078.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248079.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248080.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n")

		jobs2 = ("\n\n"
			"Job ID               Username Queue    Jobname    SessID NDS   TSK Memory Time  S Time\n"
			"-------------------- -------- -------- ---------- ------ ----- --- ------ ----- - -----\n"
			"6248067.cronos.e12.p rmuenzer farmqe   param_hf_u  16565     1  --   30mb 02:00 R 00:23   dallas/3\n"
			"6248068.cronos.e12.p rmuenzer farmqe   param_hf_u  16995     1  --   30mb 02:00 R 00:22   dallas/4\n"
			"6248069.cronos.e12.p rmuenzer farmqe   param_hf_u  17467     1  --   30mb 02:00 R 00:20   dallas/5\n"
			"6248070.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 R 00:01    -- \n"
			"6248071.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 R 00:01    -- \n"
			"6248072.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 R 00:00    -- \n"
			"6248073.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 R   --     -- \n"
			"6248074.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 R   --     -- \n"
			"6248075.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248076.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248077.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248078.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248079.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- ")

		jobs3 = ("\n\n"
			"Job ID               Username Queue    Jobname    SessID NDS   TSK Memory Time  S Time\n"
			"-------------------- -------- -------- ---------- ------ ----- --- ------ ----- - -----\n"
			"6248067.cronos.e12.p rmuenzer farmqe   param_hf_u  16565     1  --   30mb 02:00 R 00:23   iddallas/3\n"
			"6248068.cronos.e12.p rmuenzer farmqe   param_hf_u  16995     1  --   30mb 02:00 R 00:22   dallas/4\n"
			"6248069.cronos.e12.p rmuenzer farmqe   param_hf_u  17467     1  --   30mb 02:00 R 00:20   dallas/5\n"
			"6248070.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248071.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248072.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248073.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248074.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248075.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248076.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248077.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248078.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248079.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248081.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248082.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248083.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 Q   --     -- \n"
			"6248084.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 H   --     -- \n"
			"6248085.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 H   --     -- \n"
			"6248086.cronos.e12.p rmuenzer farmqe   param_hf_u    --      1  --   30mb 02:00 H   --     -- \n")

		jobs4 = ("\n\n"
			"Job ID               Username Queue    Jobname    SessID NDS   TSK Memory Time  S Time\n"
			"-------------------- -------- -------- ---------- ------ ----- --- ------ ----- - -----\n")

		jobs_list = []
		users_list = collections.OrderedDict()
		users_list['ALL'] = UserData('ALL')
		users_list['rmuenzer'] = UserData('rmuenzer')

		update.parse_qstat(jobs1, jobs_list)
		update.validate_jobs_list(jobs_list, users_list)
		update.cleanup_jobs_list(jobs_list, users_list)
		exp_len = 17
		self.assertEqual(len(jobs_list), exp_len)
		self.assertEqual(jobs_list[0].jid, 6248064)
		self.assertEqual(jobs_list[exp_len-1].jid, 6248080)
		test_user = users_list['rmuenzer']
		self.assertEqual(test_user.njobsT, exp_len)
		self.assertEqual(test_user.njobsQ, 11)
		self.assertEqual(test_user.njobsR, 6)
		self.assertEqual(test_user.njobsH, 0)

		update.parse_qstat(jobs2, jobs_list)
		update.validate_jobs_list(jobs_list, users_list)
		update.cleanup_jobs_list(jobs_list, users_list)
		exp_len = 13
		self.assertEqual(len(jobs_list), exp_len)
		self.assertEqual(jobs_list[0].jid, 6248067)
		self.assertEqual(jobs_list[exp_len-1].jid, 6248079)
		test_user = users_list['rmuenzer']
		self.assertEqual(test_user.njobsT, exp_len)
		self.assertEqual(test_user.njobsQ, 5)
		self.assertEqual(test_user.njobsR, 8)
		self.assertEqual(test_user.njobsH, 0)

		update.parse_qstat(jobs3, jobs_list)
		update.validate_jobs_list(jobs_list, users_list)
		update.cleanup_jobs_list(jobs_list, users_list)
		exp_len = 19
		self.assertEqual(len(jobs_list), exp_len)
		self.assertEqual(jobs_list[0].jid, 6248067)
		self.assertEqual(jobs_list[exp_len-1].jid, 6248086)
		test_user = users_list['rmuenzer']
		self.assertEqual(test_user.njobsT, exp_len)
		self.assertEqual(test_user.njobsQ, 13)
		self.assertEqual(test_user.njobsR, 3)
		self.assertEqual(test_user.njobsH, 3)

		update.parse_qstat(jobs4, jobs_list)
		update.validate_jobs_list(jobs_list, users_list)
		update.cleanup_jobs_list(jobs_list, users_list)
		exp_len = 0
		self.assertEqual(len(jobs_list), exp_len)
		test_user = users_list['rmuenzer']
		self.assertEqual(test_user.njobsT, 0)
		self.assertEqual(test_user.njobsQ, 0)
		self.assertEqual(test_user.njobsR, 0)
		self.assertEqual(test_user.njobsH, 0)

	def test_update_slurm(self):
		jobs1 = (
			"JOBID USER PARTITION TIME_LIMIT STATE TIME\n"
			"7574 rlalik farmq 10:00 RUNNING 0:15\n"
			"7576 rlalik farmq 10:00 RUNNING 0:15\n")

		jobs2 = (
			"JOBID USER PARTITION TIME_LIMIT STATE TIME\n"
			"7574 rlalik farmq 10:00 RUNNING 0:15\n"
			"7576 rlalik farmq 10:00 RUNNING 0:15\n"
			"7577 tkunz farmq 10:00 RUNNING 0:15\n"
			"7578 tkunz farmq 10:00 RUNNING 0:15\n"
			"7579 tkunz farmq 10:00 RUNNING 0:15\n"
			"7580 tkunz farmq 10:00 RUNNING 0:15\n")

		jobs3 = (
			"JOBID USER PARTITION TIME_LIMIT STATE TIME\n"
			"7576 rlalik farmq 10:00 RUNNING 0:15\n"
			"7578 tkunz farmq 10:00 RUNNING 0:15\n"
			"7579 tkunz farmq 10:00 RUNNING 0:15\n"
			"7580 tkunz farmq 10:00 RUNNING 0:15\n")

		jobs_list = []
		users_list = collections.OrderedDict()
		users_list['ALL'] = UserData('ALL')

		fs_obj, farm_obj = update.import_modules("", None, "slurm")

		""" test 1 """
		farm_obj.data = jobs1
		update.parse_data(fs_obj, farm_obj, jobs_list, users_list)

		exp_len = 2
		self.assertEqual(len(jobs_list), exp_len)
		self.assertEqual(jobs_list[0].jid, 7574)
		self.assertEqual(jobs_list[exp_len-1].jid, 7576)
		test_user = users_list['rlalik']
		self.assertEqual(test_user.njobsT, exp_len)
		self.assertEqual(test_user.njobsQ, 0)
		self.assertEqual(test_user.njobsR, 2)
		self.assertEqual(test_user.njobsH, 0)

		""" test 2 """
		farm_obj.data = jobs2
		update.parse_data(fs_obj, farm_obj, jobs_list, users_list)

		exp_len = 6
		self.assertEqual(len(jobs_list), exp_len)
		self.assertEqual(jobs_list[0].jid, 7574)
		self.assertEqual(jobs_list[exp_len-1].jid, 7580)
		test_user = users_list['rlalik']
		self.assertEqual(test_user.njobsT, 2)
		self.assertEqual(test_user.njobsQ, 0)
		self.assertEqual(test_user.njobsR, 2)
		self.assertEqual(test_user.njobsH, 0)
		test_user = users_list['tkunz']
		self.assertEqual(test_user.njobsT, 4)
		self.assertEqual(test_user.njobsQ, 0)
		self.assertEqual(test_user.njobsR, 4)
		self.assertEqual(test_user.njobsH, 0)

		""" test 3 """
		farm_obj.data = jobs3
		update.parse_data(fs_obj, farm_obj, jobs_list, users_list)

		exp_len = 4
		self.assertEqual(len(jobs_list), exp_len)
		self.assertEqual(jobs_list[0].jid, 7576)
		self.assertEqual(jobs_list[exp_len-1].jid, 7580)
		test_user = users_list['rlalik']
		self.assertEqual(test_user.njobsT, 1)
		self.assertEqual(test_user.njobsQ, 0)
		self.assertEqual(test_user.njobsR, 1)
		self.assertEqual(test_user.njobsH, 0)
		test_user = users_list['tkunz']
		self.assertEqual(test_user.njobsT, 3)
		self.assertEqual(test_user.njobsQ, 0)
		self.assertEqual(test_user.njobsR, 3)
		self.assertEqual(test_user.njobsH, 0)
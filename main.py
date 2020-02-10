from indeed import get_jobs as get_indeed_jobs
from stacko import get_jobs as get_stacko_jobs
from save import save_to_file

indeed_jobs = get_indeed_jobs()
stacko_jobs = get_stacko_jobs()
jobs = indeed_jobs + stacko_jobs
save_to_file(jobs)

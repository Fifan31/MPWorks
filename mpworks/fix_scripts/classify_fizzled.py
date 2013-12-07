from collections import defaultdict
import os
from fireworks.core.launchpad import LaunchPad

__author__ = 'Anubhav Jain'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Anubhav Jain'
__email__ = 'ajain@lbl.gov'
__date__ = 'Nov 11, 2013'

if __name__ == '__main__':
    module_dir = os.path.dirname(os.path.abspath(__file__))
    lp_f = os.path.join(module_dir, 'my_launchpad.yaml')
    lpdb = LaunchPad.from_file(lp_f)

    except_dict = defaultdict(int)
    fizzled_fws = []


    for f in lpdb.fireworks.find({"state": "FIZZLED"}, {'fw_id': 1}):
        fizzled_fws.append(f['fw_id'])

    for l in lpdb.launches.find({"state": "FIZZLED", "action":{"$ne": None}}, {"action":1, 'fw_id': 1, 'time_start': 1, 'launch_dir':1}):

        if l['fw_id'] in fizzled_fws:
            except_str = l['action']['stored_data'].get('_exception')
            if 'Disk quota exceeded' in except_str:
                 except_dict['DISK_QUOTA_EXCEEDED'] = except_dict['DISK_QUOTA_EXCEEDED']+1
            elif 'No such file' in except_str:
                # this is due to missing CHGCAR from Michael's old runs
                except_dict['NO_SUCH_FILE'] = except_dict['NO_SUCH_FILE']+1
            elif 'IMPROPER PARSING' in except_str:
                except_dict['IMPROPER_PARSING'] = except_dict['IMPROPER_PARSING']+1
            elif 'get valid results from relaxed run' in except_str:
                except_dict['INVALID_RESULTS'] = except_dict['INVALID_RESULTS']+1
            elif 'dir does not exist!' in except_str:
                except_dict['MISSING_DIR'] = except_dict['MISSING_DIR']+1
            elif 'Stale NFS file handle' in except_str:
                except_dict['STALE_NFS'] = except_dict['STALE_NFS']+1
            elif 'File exists' in except_str:
                except_dict['FILE_EXISTS'] = except_dict['FILE_EXISTS']+1
            elif 'MemoryError' in except_str:
                except_dict['MEMORY_ERROR'] = except_dict['MEMORY_ERROR']+1
            elif 'DB insertion successful, but don\'t know how to fix' in except_str:
                except_dict['NO_FIX'] = except_dict['NO_FIX']+1
                print l['launch_dir']
            elif 'Poscar.from_string' in except_str and 'chunks[0]' in except_str:
                except_dict['POSCAR_PARSE'] = except_dict['POSCAR_PARSE']+1
            elif 'TypeError: integer argument expected, got float':
                except_dict['MAXRUN_TYPE'] = except_dict['MAXRUN_TYPE']+1
            else:
                except_dict[except_str] = except_dict[except_str]+1

    print '-----'
    for k, v in except_dict.iteritems():
        print {"{}\t{}".format(v, k)}
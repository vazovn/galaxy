#!/cluster/software/VERSIONS/python2-2.7.10/bin/python
def exec_before_job(app, inp_data, out_data, param_dict, tool):
    out_data['output1'].name = out_data['output1'].name + " [ ALIGNMENT INFO ]"
    out_data['output2'].name = out_data['output2'].name + " [ PILEUP ]"
    out_data['output3'].name = out_data['output3'].name + " [ CUSTOM TRACK ]"

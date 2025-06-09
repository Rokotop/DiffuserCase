import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    
    plt.style.use('mystyle.mplstyle')
    
    models = ['kOmegaSST','LaunderSharmaKE','SpalartAllmaras','kEpsilonPhitF']
    model_names = ['$k-\omega$ SST',r'Launder Sharma $k-\varepsilon$',
                    'Spalart Allmaras',r'$k-\varepsilon-\phi-f$']
    colors = ['black', 'blue', 'red', 'green']
    lineStyles = ['-', '--', ':', '-.']
    
    # ================================== Diffuser profiles ================================== #
    sec_loc_full = np.loadtxt('SetsLocs.csv',skiprows=1,delimiter=',')
    sec_loc = sec_loc_full[:,1]
    sec_code = sec_loc_full[:,0]
    var_locs = [2, 5, 8, 6]
    vars = ['Ux','u2','v2','uv']
    exp_name = ['m__U','f_uu','f_vv','f_uv']
    x_lable = ['$x/H+10U/{{U}_{\mathrm{b}}}$',
            '$x/H+500\overline{{u}^{2}}/{{U}_{\mathrm{b}}}^{2}$',
            '$x/H+500\overline{{v}^{2}}/{{U}_{\mathrm{b}}}^{2}$',
            '$x/H+500\overline{uv}/{{U}_{\mathrm{b}}}^{2}$']
    power = [1, 2, 2, 2]
    u_b = 1.8
    u_non_dim = np.power(u_b,power)
    factor = [10, 500, 500, 500]
    sampleTime = []
    case_dir = []
    
    # Diffuser boundaries
    H = 1
    Hp=0.01 #kept so plotting is consistent with previous version
    L = np.loadtxt('NodesLower')/Hp
    L = L[L[:, 0].argsort()]
    U = np.loadtxt('NodesUpper')/Hp

    for i in range(len(vars)):  
        fig, ax = plt.subplots(figsize=(12,3))
        ax.axis([-10, 50, -0.01, 4.74])
        ax.set_xlabel(x_lable[i], fontsize=15)
        ax.set_ylabel('$y/H$', fontsize=15)
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)

        # Diffuser boundaries
        ax.plot(U[:,0], U[:,1], linewidth=1.5, color='k')
        ax.plot(L[:,0], L[:,1], linewidth=1.5, color='k')
        x = L[:,0]
        y1 = L[:,1]
        ax.fill_between(x, y1, color=[0.8,0.8,0.8])
        
        all_profiles = np.nonzero(sec_loc_full[:,i+2])[0]
#        print(sec_loc_full[:,i+2])
        selected_profiles = all_profiles[[0,2,3,5,7,9,10,11]]
        #print(selected_profiles[0])
        for j in selected_profiles:
            for k in range(len(models)):                
                if i == 0 and j == selected_profiles[0]: #find the writeTime only once
                    case_dir.append('../' + models[k] + '/postProcessing/')
                   # sampleTime.append(os.listdir(case_dir[k] + 'sample/')[0])
                   # sampleTime.append(os.listdir(case_dir[k] + 'singleGraph' + str(sec_code[j]).replace('.0','') + "/")[0])
                    sample_dir = case_dir[k] + 'singleGraph' + str(sec_code[j]).replace('.0','') + "/"
                    all_times = [d for d in os.listdir(sample_dir) if d.replace('.', '', 1).isdigit()]
                    latest_time = sorted(all_times, key=lambda x: float(x))[-1]
                    sampleTime.append(latest_time)
                    print(latest_time)
                    print(sample_dir)


                #Data = np.loadtxt(case_dir[k] + 'sample/' + sampleTime[k] + '/x_by_H_' 
                #                   + str(sec_code[j]).replace('.0','')
                #                   + '_p_U_turbulenceProperties:R.xy')
                Data = np.loadtxt(case_dir[k] + 'singleGraph' + str(sec_code[j]).replace('.0','') + "/" +  sampleTime[k] + '/line_p_U_turbulenceProperties:R.xy')
           #     print(j)
                ax.plot(sec_loc[j]+factor[i]*Data[:,var_locs[i]]/u_non_dim[i],
                        Data[:,0]/H, linestyle=lineStyles[k], color=colors[k],
                        label=model_names[k])
#                if j==0:
#                    print(Data[:,0]/H)
#                    print(sec_loc[j]+factor[i]*Data[:,var_locs[i]]/u_non_dim[i])
#                if j==12:
#                    print(Data[:,0]/H)
            
            Exp = np.loadtxt('../Experiment/' + exp_name[i] + '%.x'
                             + str(sec_code[j]).replace('.0',''))
            ax.plot(sec_loc[j]+factor[i]*Exp[:,1], Exp[:,0], marker='o', linestyle='None',
                    markersize=4, color='b', markerfacecolor='None', label='Experiment')
          #  if j==0:
          #      print(Exp[:,0])
        
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[0:len(models)+1], labels[0:len(models)+1], loc='lower left',
                  edgecolor='k', framealpha=1, labelspacing = 0.25, fontsize=13)
        fig.savefig('../Figures/' + vars[i] + '.pdf', bbox_inches='tight') #+ str(sec_code[j]).replace('.0','')
    # ======================================================================================= #


    # ====================================== Cf and Cp ====================================== #
    rho = 1
    num_name = ['wallShearStress','p']
    exp_name = ['cf','cp']
    exp_name_loc = ['00', '10']
    wall_name = ['lower', 'upper']
    y_axis_lims = [[-0.002, 0.008], [-0.2, 1.0]]
    y_label = ['$C_f$','$C_p$']
    for i in range(len(num_name)): #Cf and Cp
        for j in range(len(wall_name)): # lower and upper walls
            fig, ax = plt.subplots()
            ax.set_xlim([-10,70])
            ax.set_ylim(y_axis_lims[i])
            ax.set_xlabel('$x/H$')
            ax.set_ylabel(y_label[i])
            
            for k in range(len(models)):
                Data = np.loadtxt(case_dir[k] + 'surfaceSampling/' + sampleTime[k] + '/' + num_name[i] 
                                  + '_' + wall_name[j] + 'Wall.raw', skiprows=2)
                if i == 0:
                    fp = -Data[:,3]
                else:
                    pref = np.loadtxt(case_dir[k] + 'singleGraph-1_7/' + sampleTime[k] + '/' 
                                      'line_p_U_turbulenceProperties:R.xy')
                    pref_mean = np.mean(pref[:,1])
                    fp = Data[:,3] - pref_mean
                
                ax.plot(Data[:,0]/H, fp/(0.5*rho*u_b**2), linestyle=lineStyles[k],
                        color=colors[k], label=model_names[k])
            
            exp = np.loadtxt('../Experiment/g_' + exp_name[i] + '%.y' + exp_name_loc[j])
            ax.plot(exp[:,0], exp[:,1], marker='o', linestyle='None', color='b',
                    markersize=6, markerfacecolor='None', label='Experiment')
            
            ax.legend(loc='best', edgecolor='k', framealpha=1, labelspacing = 0.25)              
            fig.savefig('../Figures/' + exp_name[i] + '_' + wall_name[j] + 'Wall.pdf',
                        bbox_inches='tight')
    # ======================================================================================= #


    # =================================== Separation zone =================================== #
    fig, ax = plt.subplots(figsize=(12,3))
    ax.axis([-10, 50, -0.01, 4.74])
    ax.set_xlabel('$x/H$')
    ax.set_ylabel('$y/H$')
    ax.set_xlabel(x_lable[i], fontsize=15)
    ax.set_ylabel('$y/H$', fontsize=15)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)    
    
    # Diffuser boundaries
    ax.plot(U[:,0], U[:,1], linewidth=1.5, color='k')
    ax.plot(L[:,0], L[:,1], linewidth=1.5, color='k')
    ax.fill_between(x, y1, color=[0.8,0.8,0.8])
    for k in range(len(models)):
        data = np.loadtxt(case_dir[k] + 'interface/' + sampleTime[k] + '/U_interface.raw')
        ax.plot(data[:,0]/H, data[:,1]/H, linestyle='None', color=colors[k],
                marker='.', markersize=3, label=model_names[k])
    
    exp = np.loadtxt('../Experiment/separation',skiprows=1, delimiter=',')
    ax.plot(exp[:,0], exp[:,1], marker='o', linestyle='None', markersize=6,
            color='b', markerfacecolor='None', label='Experiment')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[0:len(models)+1], labels[0:len(models)+1], loc='lower left',
                edgecolor='k', framealpha=1, labelspacing = 0.25, fontsize=13)
    fig.savefig('../Figures/separation.pdf', bbox_inches='tight')
    # ======================================================================================= #

    plt.show()


if __name__ == '__main__':
    main()

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.lines as lines
import vdj.viz
import vdj.io
vdj.viz.plotting_style()

# Load the data with long-form looping events and restrict to relevant sets.
data = pd.read_csv('../../data/compiled_loop_freq_bs.csv',       
                   comment='#')
counts = data[(data['salt']=='Mg') & (data['hmgb1']==80) & 
        (data['percentile']==95.0) & (data['mutant']!='12CodC6A')]

# Load the dwell times
dwell = pd.read_csv('../../data/compiled_dwell_times.csv', comment='#')
dwell = dwell[(dwell['salt']=='Mg') & (dwell['hmgb1']==80) & (dwell['mutant']!='12CodC6A')]

# Compute the median dwell time
median_dwell = dwell.groupby('mutant')['dwell_time_min'].median().reset_index()
dwell_25 = dwell.groupby('mutant')['dwell_time_min'].quantile(0.25).reset_index()
dwell_75 = dwell.groupby('mutant')['dwell_time_min'].quantile(0.75).reset_index()

# Load all cutting probability estimates taking gaussian approximation.
cut_data = pd.read_csv('../../data/pooled_cutting_probability.csv', comment='#')
cut_data = cut_data[(cut_data['hmgb1'] == 80) & (cut_data['salt']=='Mg') & (cut_data['mutant']!='12CodC6A')]

# Load the precomputed posterior distributioons
cut_posts = pd.read_csv('../../data/pooled_cutting_probability_posteriors.csv', 
                        comment='#')
cut_posts = cut_posts[(cut_posts['hmgb1']==80) & (cut_posts['salt']=='Mg') & (cut_posts['mutant']!='12CodC6A')]

# Load the significance testing for p_values less than 0.05
sig_loop = pd.read_csv('../../data/looping_frequency_p_values.csv', comment='#')
sig_loop = sig_loop[(sig_loop['p_value'] <= 0.05) & (sig_loop['mutant']!='CodC6A')]

sig_dwell = pd.read_csv('../../data/dwell_time_p_values.csv', comment='#')
sig_dwell = sig_dwell[(sig_dwell['p_value'] <= 0.05) & (sig_dwell['mutant']!='CodC6A')]

sig_cuts = pd.read_csv('../../data/cutting_probability_p_values.csv', comment='#')
sig_cuts = sig_cuts[(sig_cuts['p_value'] <= 0.05) & (sig_cuts['mutant']!='CodC6A')]
# Get the reference seq
ref = vdj.io.endogenous_seqs()['WT12rss']
ref_seq = ref[0]
ref_idx = ref[1]

# Include the mutant id information
wt_val = counts[counts['mutant']=='WT12rss']['loops_per_bead'].values[0]
wt_loop_low = counts[counts['mutant']=='WT12rss']['low'].values[0]
wt_loop_high = counts[counts['mutant']=='WT12rss']['high'].values[0]

wt_cut = cut_data[cut_data['mutant']=='WT12rss']['mode'].values[0]
wt_std = cut_data[cut_data['mutant']=='WT12rss']['std'].values[0]

wt_dwell = median_dwell[median_dwell['mutant']=='WT12rss']['dwell_time_min'].values[0]
wt_dwell_25 = dwell_25[dwell_25['mutant']=='WT12rss']['dwell_time_min'].values[0]
wt_dwell_75 = dwell_75[dwell_75['mutant']=='WT12rss']['dwell_time_min'].values[0]

for m in counts['mutant'].unique():
    seq = vdj.io.mutation_parser(m)
    counts.loc[counts['mutant']==m, 'n_muts'] = seq['n_muts']
    cut_data.loc[cut_data['mutant']==m, 'n_muts'] = seq['n_muts']
    median_dwell.loc[median_dwell['mutant']==m, 'n_muts'] = seq['n_muts']
    sig_loop.loc[sig_loop['mutant']==m, 'n_muts'] = seq['n_muts']
    sig_dwell.loc[sig_dwell['mutant']==m, 'n_muts'] = seq['n_muts']
    sig_cuts.loc[sig_cuts['mutant']==m, 'n_muts'] = seq['n_muts']

    if m in median_dwell['mutant'].unique():
        median_dwell.loc[median_dwell['mutant']==m, 'dwell_25'] = dwell_25[dwell_25['mutant']==m]['dwell_time_min'].values[0]
        median_dwell.loc[median_dwell['mutant']==m, 'dwell_75'] = dwell_75[dwell_75['mutant']==m]['dwell_time_min'].values[0]

    # Find the x and mutation identity
    loc = np.argmax(ref_idx != seq['seq_idx'])
    mut = seq['seq'][loc]
    counts.loc[counts['mutant']==m, 'pos'] = loc
    counts.loc[counts['mutant']==m, 'base'] = mut
    median_dwell.loc[median_dwell['mutant']==m, 'pos'] = loc
    median_dwell.loc[median_dwell['mutant']==m, 'base'] = mut
    sig_loop.loc[sig_loop['mutant']==m, 'pos'] = loc
    sig_loop.loc[sig_loop['mutant']==m, 'base'] = mut
    sig_dwell.loc[sig_dwell['mutant']==m, 'pos'] = loc
    sig_dwell.loc[sig_dwell['mutant']==m, 'base'] = mut
    sig_cuts.loc[sig_cuts['mutant']==m, 'pos'] = loc
    sig_cuts.loc[sig_cuts['mutant']==m, 'base'] = mut

# Keep the single point mutants
points = counts[(counts['n_muts'] == 1) & (counts['mutant'] != 'V4-55')].copy()
points_cut = cut_data[(cut_data['n_muts'] == 1) & (cut_data['mutant'] != 'V4-55')].copy()
points_dwell = median_dwell[(median_dwell['n_muts']==1) & (median_dwell['mutant'] != 'V4-55')].copy()
sig_loop = sig_loop[(sig_loop['n_muts'] == 1) & (sig_loop['mutant'] != 'V4-55')].copy()
sig_dwell = sig_dwell[(sig_dwell['n_muts'] == 1) & (sig_dwell['mutant'] != 'V4-55')].copy()
sig_cuts = sig_cuts[(sig_cuts['n_muts'] == 1) & (sig_cuts['mutant'] != 'V4-55')].copy()

for m in points_cut['mutant'].unique():
        seq = vdj.io.mutation_parser(m)
        loc = np.argmax(ref_idx != seq['seq_idx'])
        mut = seq['seq'][loc]
        points_cut.loc[points_cut['mutant']==m, 'pos'] = loc
        points_cut.loc[points_cut['mutant']==m, 'base'] = mut
        _d = points_cut[points_cut['mutant']==m]

# Set offsets for p_value significance
for j, sig in enumerate([sig_loop, sig_dwell, sig_cuts]):
        for p,d in sig.groupby('pos'):
                if len(d) == 1:
                        sig.loc[sig['pos']==p,'x_offset'] = 0
                else:
                        offset = -0.5
                        for base, d_pos in d.groupby('base'):
                                sig.loc[(sig['pos']==p) & (sig['base']==base), 'x_offset'] = offset
                                offset+=1

#%%
# zshift in stickplots allow plot colors to show up more prominently
zshift = 100
posterior_list = ['WT12rss', '12HeptC3G', '12HeptC3T', '12SpacC4G', '12NonA4C', '12SpacG10T']
posterior_shift = {'WT12rss': 0, 
                   '12HeptC3G': 0.1, 
                   '12HeptC3T': 0.2, 
                   '12SpacC4G': 0.3, 
                   '12NonA4C': 0.4,
                   '12SpacG10T': 0.5}
post_colors = {'12HeptC3G' : '#E10C00', 
                '12HeptC3T' : '#BF3030', 
                '12SpacC4G' : '#A24F59', 
                '12NonA4C' : '#7D778E', 
                'WT12rss' :  'slategrey', #599DC1', 
                '12SpacG10T' : '#679CE8'} #'#38C2F2'}
post_zorder = {'12HeptC3G' : 2, 
                '12HeptC3T' : 3, 
                '12SpacC4G' : 4, 
                '12NonA4C' : 5, 
                'WT12rss' :  1,
                '12SpacG10T': 6}
 
post_hatch = {'12HeptC3G' : None, 
                '12HeptC3T' : None, 
                '12SpacC4G' : None, 
                '12NonA4C' : None, 
                'WT12rss' : None, 
                '12SpacG10T' : None}
plot_offset = dict(zip(posterior_list[::-1], np.arange(0.0, 0.2, 0.2/(len(posterior_list)))))

bar_width = 0.75
fig_loop, ax_loop = plt.subplots(1, 1, figsize=(8.2, 2.3), facecolor='white')
plt.subplots_adjust(hspace=0.2)

colors = {'A':'#E10C00', 'T':'#38C2F2', 'C':'#278C00', 'G':'#5919FF'}
shift = {'A':0, 'T':0, 'C':0, 'G':0}
hshift = {'A':-0.2,  'T':0.2, 'C':-0.1, 'G':0.1}


p = points
a = ax_loop
v = 'loops_per_bead'
vshift = 0.019

for g, d in p.groupby('pos'):
        d = d.copy()
        if len(d) == 1:
                base = d['base'].unique()
                if type(base) != str:
                        base = base[0]
                a.plot(g + 1 + hshift[base], d[v], marker='o', color=colors[base], lw=0.75, 
                        ms=10, linestyle='none', label='__nolegend__', zorder=zshift,
                        markerfacecolor='white', alpha=0.7)
                if (base == 'T') | (base == 'A'):
                        shift = 0.05
                else:
                        shift = 0 
                a.annotate(base , xy=(g + 0.78 + shift + hshift[base], d[v] - vshift), 
                        color=colors[base], zorder=zshift, size=9,  label='__nolegend__', 
                        clip_on=False)
                a.vlines(g + 1 + hshift[base], d['low'], d['high'], zorder=zshift,
                        alpha=0.7, color=colors[base], lw=1.5, label='__nolegend__')
        else:
                zorder = len(d) + 2 
                d[f'abs_{v}'] = np.abs(d[v])
                d.sort_values(f'abs_{v}', inplace=True)
                for i in range(len(d)):
                        _d = d.iloc[i]
                        base = _d['base']
                        if type(base) != str:
                                base = base[0]
                        a.vlines(g + 1 + hshift[base], _d['low'], _d['high'],
                                color=colors[base], lw=1.5, label='__nolegend__',
                                zorder=zorder+zshift, alpha=0.7)

                        if (base == 'T') | (base == 'A'):
                                shift = 0.05
                        else:
                                shift = 0 

                        a.plot(g + 1 + hshift[base], _d[v], marker='o', color=colors[base], lw=0.75, 
                        ms=10, linestyle='none', label='__nolegend__', 
                        markerfacecolor='white', zorder=zorder+zshift, alpha=0.7)
                        a.annotate(base , xy=(g + 0.78 + shift + hshift[base], _d[v] - vshift), color=colors[base], #, markeredgewidth=0.5,
                                size=9,  label='__nolegend__', zorder=zorder+zshift, clip_on=False)

        zorder -= 1

x_offset = {'A':-0.15, 'C':-0.05, 'G':0.05, 'T':0.15}
for g,d in sig_loop.groupby('mutant'):
        base = d['base'].values[0]
        ax_loop.text(d['pos']+0.82+0.5*d['x_offset'], 0.58, '*', fontsize=16,
                        color=colors[base])

wt_x = np.linspace(0, 30, 1000)
ax_loop.fill_between(wt_x, wt_loop_low, wt_loop_high, facecolor='grey', 
                        zorder=zshift, alpha=0.4)

# Previous y positions were -0.84 and -0.72
line_loop1 = lines.Line2D([7.5, 7.5], [-0.12, -0.02], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_loop2 = lines.Line2D([19.5, 19.5], [-0.12, -0.02], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_loop3 = lines.Line2D([7.5, 7.5], [0.67, 0.75], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_loop4 = lines.Line2D([19.5, 19.5], [0.67, 0.75], clip_on=False, alpha=1,
                    linewidth=1, color='k')

line_loop = [line_loop1, line_loop2, line_loop3, line_loop4]

for a in [ax_loop]:
        _ = a.set_xticks(np.arange(1, 29))
        a.set_xlim([0.5, 28.5])
        a.vlines(0.5, -0.65, 1.0, linewidth=4, zorder=0) #, color='#f5e3b3')
        for i in range(1, 29, 2):
                a.axvspan(i-0.5, i+0.5, color='white',
                        alpha=0.65, linewidth=0, zorder=-1)

ax_loop.hlines(wt_val, 0, 29, color='k', linestyle=':')

for a,l in zip([ax_loop],[line_loop]):
        _ = a.set_xticklabels([])
        _ = a.set_xticklabels(list(ref_seq))
        for _l in l:
                _ = a.add_line(_l)

_ = ax_loop.set_xticklabels([])
_ = ax_loop.set_xticklabels(list(ref_seq))
ax_loop.add_line(line_loop1)
ax_loop.add_line(line_loop2)
ax_loop.add_line(line_loop3)
ax_loop.add_line(line_loop4)

ax_loop.text(-0.05, -0.07, 'ref:', ha='center', va='center', fontsize=10)

ax_loop.set_xlabel(None)
ax_loop.set_ylim([-0.01, 0.65])
ax_loop.set_xlim([0.7, 28.5])
ax_loop.set_ylabel('loop frequency', fontsize=12)
ax_loop.set_title('Heptamer', loc='left')
ax_loop.set_title('Spacer         ') # Spaces are ad-hoc positioning
ax_loop.set_title('Nonamer', loc='right')

ax_loop.spines['left'].set_visible(False)

# Add Figure Panels. 
plt.savefig('./SubFigXC_point_loop.pdf', facecolor='white',
                 bbox_inches='tight')

#%%
bar_width = 0.75
fig_dwell, ax_dwell = plt.subplots(1, 1, figsize=(8.2, 2.3), facecolor='white')
plt.subplots_adjust(hspace=0.2)

colors = {'A':'#E10C00', 'T':'#38C2F2', 'C':'#278C00', 'G':'#5919FF'}
shift = {'A':0, 'T':0, 'C':0, 'G':0}
hshift = {'A':-0.2,  'T':0.2, 'C':-0.1, 'G':0.1}

p = points_dwell
a = ax_dwell
v = 'dwell_time_min'
vshift = 0.25

for g, d in p.groupby('pos'):
        d = d.copy()
        if len(d) == 1:
                        base = d['base'].unique()
                        if type(base) != str:
                                base = base[0]
                        a.plot(g + 1 + hshift[base], d[v], marker='o', color=colors[base], lw=0.75, 
                                ms=10, linestyle='none', label='__nolegend__', zorder=zshift,
                                markerfacecolor='white', alpha=0.7)
                        if (base == 'T') | (base == 'A'):
                                shift = 0.05
                        else:
                                shift = 0 
                        a.annotate(base , xy=(g + 0.78 + shift + hshift[base], d[v] - vshift), 
                                color=colors[base], zorder=zshift, size=9,  label='__nolegend__', 
                                clip_on=False)
                        a.vlines(g + 1 + hshift[base], d['dwell_25'], d['dwell_75'], alpha=0.7,
                                zorder=zshift, color=colors[base], lw=1.5, label='__nolegend__')
        else:
                zorder = len(d) + 2 
                d[f'abs_{v}'] = np.abs(d[v])
                d.sort_values(f'abs_{v}', inplace=True)
                for i in range(len(d)):
                        _d = d.iloc[i]
                        base = _d['base']
                        if type(base) != str:
                                base = base[0]
                        a.vlines(g + 1 + hshift[base], _d['dwell_25'], _d['dwell_75'],
                                color=colors[base], lw=1.5, label='__nolegend__',
                                zorder=zorder+zshift, alpha=0.7)
                        if (base == 'T') | (base == 'A'):
                                shift = 0.05
                        else:
                                shift = 0 

                        a.plot(g + 1 + hshift[base], _d[v], marker='o', color=colors[base], lw=0.75, 
                        ms=10, linestyle='none', label='__nolegend__', 
                        markerfacecolor='white', zorder=zorder+zshift, alpha=0.7)
                        a.annotate(base , xy=(g + 0.78 + shift + hshift[base], _d[v] - vshift), color=colors[base], #, markeredgewidth=0.5,
                                size=9,  label='__nolegend__', zorder=zorder+zshift, clip_on=False)

        zorder -= 1

x_offset = {'A':-0.15, 'C':-0.05, 'G':0.05, 'T':0.15}
for g,d in sig_dwell.groupby('mutant'):
        base = d['base'].values[0]
        ax_dwell.text(d['pos']+0.82+0.5*d['x_offset'], 8.05, '*', fontsize=16,
                        color=colors[base])

wt_x = np.linspace(0, 30, 1000)
ax_dwell.vlines(1, wt_dwell_25, wt_dwell_75, zorder=zshift,
                color='k', lw=1.5)
 
# Previous y positions were -0.84 and -0.72
line_dwell1 = lines.Line2D([7.5, 7.5], [-0.2, -1.4], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_dwell2 = lines.Line2D([19.5, 19.5], [-0.2, -1.4], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_dwell3 = lines.Line2D([7.5, 7.5], [9.2, 10.2], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_dwell4 = lines.Line2D([19.5, 19.5], [9.2, 10.2], clip_on=False, alpha=1,
                    linewidth=1, color='k')

line_dwell = [line_dwell1, line_dwell2, line_dwell3, line_dwell4]

for a in [ax_dwell]:
        _ = a.set_xticks(np.arange(1, 29))
        a.set_xlim([0.5, 28.5])
        a.vlines(0.5, -0.65, 1.0, linewidth=4, zorder=0) #, color='#f5e3b3')
        for i in range(1, 29, 2):
                a.axvspan(i-0.5, i+0.5, color='white',
                        alpha=0.65, linewidth=0, zorder=-1)

ax_dwell.hlines(wt_dwell, 0, 29, color='k', linestyle=':')

for a,l in zip([ax_dwell],[line_dwell]):
        _ = a.set_xticklabels([])
        _ = a.set_xticklabels(list(ref_seq))
        for _l in l:
                _ = a.add_line(_l)

_ = ax_dwell.set_xticklabels([])
_ = ax_dwell.set_xticklabels(list(ref_seq))
ax_dwell.add_line(line_dwell3)
ax_dwell.add_line(line_dwell4)

ax_dwell.text(-0.05, -0.7, 'ref:', ha='center', va='center', fontsize=10)

ax_dwell.set_ylim([0, 9])
ax_dwell.set_xlim([0.7, 28.5])
ax_dwell.set_ylabel('dwell time [min]', fontsize=12)
ax_dwell.set_title('Heptamer', loc='left')
ax_dwell.set_title('Spacer         ') # Spaces are ad-hoc positioning
ax_dwell.set_title('Nonamer', loc='right')
ax_dwell.spines['left'].set_visible(False)

plt.savefig('./SubFigXC_point_dwell.pdf', facecolor='white',
                 bbox_inches='tight')

#%%
bar_width = 0.75
fig_cut, ax_cut = plt.subplots(2, 1, figsize=(8.2, 4.5), facecolor='white')
plt.subplots_adjust(hspace=0.2)

colors = {'A':'#E10C00', 'T':'#38C2F2', 'C':'#278C00', 'G':'#5919FF'}
shift = {'A':0, 'T':0, 'C':0, 'G':0}
hshift = {'A':-0.2,  'T':0.2, 'C':-0.1, 'G':0.1}

p = points_cut
a = ax_cut[0]
v = 'mode'
vshift = 0.03

for g, d in p.groupby('pos'):
        d = d.copy()
        if len(d) == 1:
                base = d['base'].unique()
                if type(base) != str:
                        base = base[0]
                a.plot(g + 1 + hshift[base], d[v], marker='o', color=colors[base], lw=0.75, 
                        ms=10, linestyle='none', label='__nolegend__', zorder=zshift,
                        markerfacecolor='white', alpha=0.7)
                if (base == 'T') | (base == 'A'):
                        shift = 0.05
                else:
                        shift = 0 
                a.annotate(base , xy=(g + 0.78 + shift + hshift[base], d[v] - vshift), 
                        color=colors[base], zorder=zshift, size=9,  label='__nolegend__', 
                        clip_on=False)
                a.vlines(g + 1 + hshift[base], d[v]-d['std'], d[v]+d['std'],
                        alpha=0.7, zorder=zshift, color=colors[base], lw=1.5, 
                        label='__nolegend__')
        else:
                zorder = len(d) + 2 
                d[f'abs_{v}'] = np.abs(d[v])
                d.sort_values(f'abs_{v}', inplace=True)
                for i in range(len(d)):
                        _d = d.iloc[i]
                        base = _d['base']
                        if type(base) != str:
                                base = base[0]
                        a.vlines(g + 1 + hshift[base], _d[v] - _d['std'], _d[v]+_d['std'],
                                color=colors[base], lw=1.5, label='__nolegend__',
                                zorder=zorder+zshift, alpha=0.7)
                        if (base == 'T') | (base == 'A'):
                                shift = 0.05
                        else:
                                shift = 0 

                        a.plot(g + 1 + hshift[base], _d[v], marker='o', color=colors[base], lw=0.75, 
                        ms=10, linestyle='none', label='__nolegend__', 
                        markerfacecolor='white', zorder=zorder+zshift, alpha=0.7)
                        a.annotate(base , xy=(g + 0.78 + shift + hshift[base], _d[v] - vshift), color=colors[base], #, markeredgewidth=0.5,
                                size=9,  label='__nolegend__', zorder=zorder+zshift, clip_on=False)

        zorder -= 1

x_offset = {'A':-0.15, 'C':-0.05, 'G':0.05, 'T':0.15}

for g,d in sig_cuts.groupby('mutant'):
        base = d['base'].values[0]
        ax_cut[0].text(d['pos']+0.82+0.5*d['x_offset'], 0.88, '*', fontsize=16,
                        color=colors[base])

wt_x = np.linspace(0, 30, 1000)
ax_cut[0].fill_between(wt_x, wt_cut-wt_std, wt_cut+wt_std, 
                        zorder=zshift, facecolor='grey', alpha=0.4)
 
# Previous y positions were -0.84 and -0.72
line_cut1 = lines.Line2D([7.5, 7.5], [-0.03, -0.15], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_cut2 = lines.Line2D([19.5, 19.5], [-0.03, -0.15], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_cut3 = lines.Line2D([7.5, 7.5], [1.05, 1.2], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line_cut4 = lines.Line2D([19.5, 19.5], [1.05, 1.2], clip_on=False, alpha=1,
                    linewidth=1, color='k')

line_cut = [line_cut1, line_cut2, line_cut3, line_cut4]

for a in [ax_cut[0]]:
        _ = a.set_xticks(np.arange(1, 29))
        a.set_xlim([0.5, 28.5])
        a.vlines(0.5, -0.65, 1.0, linewidth=4, zorder=0) #, color='#f5e3b3')
        for i in range(1, 29, 2):
                a.axvspan(i-0.5, i+0.5, color='white',
                        alpha=0.65, linewidth=0, zorder=-1)

ax_cut[0].hlines(wt_cut, 0, 29, color='k', linestyle=':')

for a,l in zip([ax_cut[0]],[line_cut]):
        _ = a.set_xticklabels([])
        _ = a.set_xticklabels(list(ref_seq))
        for _l in l:
                _ = a.add_line(_l)

_ = ax_cut[0].set_xticklabels([])
_ = ax_cut[0].set_xticklabels(list(ref_seq))
ax_cut[0].add_line(line_cut3)
ax_cut[0].add_line(line_cut4)

ax_cut[0].text(-0.05, -0.10, 'ref:', ha='center', va='center', fontsize=10)

ax_cut[0].set_ylim([0, 1.0])
ax_cut[0].set_xlim([0.7, 28.5])
ax_cut[0].set_ylabel(r'$p_\mathrm{cut}$', fontsize=12)
ax_cut[0].set_title('Heptamer', loc='left')
ax_cut[0].set_title('Spacer         ') # Spaces are ad-hoc positioning
ax_cut[0].set_title('Nonamer', loc='right')

df_post = cut_posts.loc[cut_posts['mutant'].isin(posterior_list)]

sort_index = dict(zip(posterior_list, range(len(posterior_list))))
df_post['rank_index'] = df_post['mutant'].map(sort_index)
df_post.sort_values(['rank_index', 'probability'], ascending=True, inplace=True)
df_post.drop('rank_index', 1, inplace=True)

for mut, mut_posts in df_post.groupby('mutant'):
        ax_cut[1].fill_between(mut_posts['probability'] , plot_offset[mut],
                        mut_posts['posterior'] + plot_offset[mut],
                        color=post_colors[mut], alpha=0.75, zorder=post_zorder[mut])
        ax_cut[1].plot(mut_posts['probability'], mut_posts['posterior'] + plot_offset[mut],
                        color='white', zorder=post_zorder[mut])
        ax_cut[1].axhline(plot_offset[mut], 0, 1.0, color=post_colors[mut], alpha=1.0, zorder=post_zorder[mut])
        if mut=='WT12rss':
                text = 'reference'
        else:
                text = mut
        ax_cut[1].text(0.95 - posterior_shift[mut], plot_offset[mut], text, backgroundcolor='#ffffff', 
                fontsize=10, color=post_colors[mut], ha="right", va="center",
                zorder=post_zorder[mut] + 1)
ax_cut[1].set_facecolor('white')
ax_cut[1].set_xlabel(r'$p_\mathrm{cut}$', fontsize=12)
ax_cut[1].set_ylim([-0.025, 0.26])
ax_cut[1].set_xlim([0.0, 1.0])
ax_cut[1].set_yticklabels([])

# Try adding an annotation. THis may be tricky.
ax_cut[1].vlines(0.56,plot_offset['WT12rss'], plot_offset['WT12rss'] + 0.06, color='k')
ax_cut[1].hlines(plot_offset['WT12rss'] + 0.06, 0.54, 0.56, color='k')
ax_cut[1].hlines(plot_offset['WT12rss'], 0.54, 0.56, color='k')
ax_cut[1].text(0.562, plot_offset['WT12rss'] + 0.025 ,r'  $\mathbf{P(p_\mathrm{cut} | n_\mathrm{loops}, n_\mathrm{cuts})}$')

plt.savefig('./SubFigXC_point_cut.pdf', facecolor='white',
                 bbox_inches='tight')


# %%

#%%
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.lines as lines
import vdj.viz 
import vdj.io 
vdj.viz.plotting_style()
# Load the data with long-form looping events and restrict to relevant sets.
data = pd.read_csv('../../data/compiled_looping_events.csv')
data = data[(data['salt']=='Mg') & (data['hmgb1']==80)]

# Load all cutting probability estimates takin ggaussian approximation.
cut_data = pd.read_csv('../../data/pooled_cutting_probability.csv')
cut_data = cut_data[(cut_data['hmgb1'] == 80) & (cut_data['salt']=='Mg')]

# Load the precomputed posterior distributioons
cut_posts = pd.read_csv('../../data/pooled_cutting_probability_posteriors.csv')
cut_posts = cut_posts[(cut_posts['hmgb1']==80) & (cut_posts['salt']=='Mg')]

# Compute the number of loops per bead
counts = data.groupby(['mutant'])[['n_loops']].agg(('sum', 'count')).reset_index()
counts['loops_per_bead'] = counts['n_loops']['sum'] / counts['n_loops']['count']

# Get the reference seq
ref = vdj.io.endogenous_seqs()['WT12rss']
ref_seq = ref[0]
ref_idx = ref[1]

# Include the mutant id information
wt_val = counts[counts['mutant']=='WT12rss']['loops_per_bead'].values[0]
wt_cut = cut_data[cut_data['mutant']=='WT12rss']['mode'].values[0]
wt_std = cut_data[cut_data['mutant']=='WT12rss']['std'].values[0]
for m in counts['mutant'].unique():
    seq = vdj.io.mutation_parser(m)
    counts.loc[counts['mutant']==m, 'n_muts'] = seq['n_muts']
    cut_data.loc[cut_data['mutant']==m, 'n_muts'] = seq['n_muts']

    # Find the x and mutation identity
    loc = np.argmax(ref_idx != seq['seq_idx'])
    mut = seq['seq'][loc]
    counts.loc[counts['mutant']==m, 'pos'] = loc
    counts.loc[counts['mutant']==m, 'base'] = mut

for m in counts['mutant'].unique():
    _d = counts[counts['mutant']==m]
    if _d['loops_per_bead'].values[0] < wt_val:
        val = 1 - _d['loops_per_bead'] / wt_val
    else:
        val = _d['loops_per_bead'] / wt_val - 1
    counts.loc[counts['mutant']==m, 'rel_diff'] = _d['loops_per_bead'].values[0] - wt_val 

# Keep the single point mutants
points = counts[counts['n_muts'] == 1].copy()
points_cut = cut_data[cut_data['n_muts'] == 1].copy()
points_cut['diff'] = points_cut['mode'] - wt_cut

for m in points_cut['mutant'].unique():
        seq = vdj.io.mutation_parser(m)
        loc = np.argmax(ref_idx != seq['seq_idx'])
        mut = seq['seq'][loc]
        points_cut.loc[points_cut['mutant']==m, 'pos'] = loc
        points_cut.loc[points_cut['mutant']==m, 'base'] = mut
        _d = points_cut[points_cut['mutant']==m]
        points_cut.loc[points_cut['mutant']==m, 'rel_diff'] = _d['mode'].values[0] - wt_cut

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
fig, ax = plt.subplots(3, 1, figsize=(8.2, 7), facecolor='white')
plt.subplots_adjust(hspace=0.2)

colors = {'A':'#E10C00', 'T':'#38C2F2', 'C':'#278C00', 'G':'#5919FF'}
shift = {'A':0,  'T':0, 'C':0, 'G':0.0}
points.sort_values('rel_diff', inplace=True)

for j, p in enumerate([points, points_cut]): 
        if j == 0:
                a = ax[0]
                v = 'rel_diff'
                vshift = 0.019
        else:
                a = ax[1]
                v = 'diff'
                vshift = 0.037

        for g, d in p.groupby('pos'):
            d = d.copy()
            if len(d) == 1:
                base = d['base'].unique()
                if type(base) != str:
                        base = base[0]
                a.plot(g + 1, d[v], marker='o', color=colors[base], lw=0.75, 
                        ms=10, linestyle='none', label='__nolegend__', 
                        markerfacecolor='white', alpha=0.8)
                if (base == 'T') | (base == 'A'):
                        shift = 0.05
                else:
                        shift = 0 
                a.annotate(base , xy=(g + 0.78 + shift, d[v] - vshift), color=colors[base], #, markeredgewidth=0.5,
                            size=9,  label='__nolegend__')
                a.vlines(g + 1, 0, d['rel_diff'], color=colors[base], lw=1.5, label='__nolegend__')
            else:
                zorder = len(d) + 2 
                d[f'abs_{v}'] = np.abs(d[v])
                d.sort_values(f'abs_{v}', inplace=True)
                for i in range(len(d)):
                    _d = d.iloc[i]
                    base = _d['base']
                    if type(base) != str:
                            base = base[0]
                    a.vlines(g + 1, 0, _d[v], color=colors[base], lw=1.5, 
                                label='__nolegend__', zorder=zorder)
                    if (base == 'T') | (base == 'A'):
                        shift = 0.05
                    else:
                        shift = 0 
        
                    a.plot(g + 1, _d[v], marker='o', color=colors[base], lw=0.75, 
                        ms=10, linestyle='none', label='__nolegend__', 
                        markerfacecolor='white', zorder=zorder, alpha=0.8)
                    a.annotate(base , xy=(g + 0.78 + shift, _d[v] - vshift), color=colors[base], #, markeredgewidth=0.5,
                           size=9,  label='__nolegend__', zorder=zorder)

                    zorder -= 1
 
# Previous y positions were -0.84 and -0.72
line1 = lines.Line2D([7.5, 7.5], [-0.4, -0.32], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line2 = lines.Line2D([19.5, 19.5], [-0.4, -0.32], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line3 = lines.Line2D([7.5, 7.5], [0.32, 0.4], clip_on=False, alpha=1,
                    linewidth=1, color='k')
line4 = lines.Line2D([19.5, 19.5], [0.32, 0.4], clip_on=False, alpha=1,
                    linewidth=1, color='k')

for n in range(0,2):
        _ = ax[n].set_xticks(np.arange(1, 29))
        ax[n].set_xlim([0.5, 28.5])
        ax[n].vlines(0.5, -0.65, 1.0, linewidth=4, zorder=0) #, color='#f5e3b3')
        ax[n].hlines(0, 0, 29, color='k', linestyle=':')
        for i in range(1, 29, 2):
                ax[n].axvspan(i-0.5, i+0.5, color='white',
                                alpha=0.65, linewidth=0, zorder=-1)

_ = ax[1].set_xticklabels([])
_ = ax[0].set_xticklabels(list(ref_seq))
ax[0].add_line(line1)
ax[0].add_line(line2)
ax[0].add_line(line3)
ax[0].add_line(line4)

ax[0].text(-1.4, -0.35, 'reference\nsequence', ha='center', va='center', fontsize=10)

# ax[0].legend(fontsize=8, ncol=5)
ax[0].set_xlabel(None)
ax[0].set_ylim([-0.3, 0.3])
ax[1].set_ylim([-0.6, 0.8])
ax[0].set_xlim([0.7, 28.5])
ax[1].set_xlim([0.7, 28.5])
ax[0].set_ylabel('$\Delta$ loop frequency', fontsize=12)
ax[1].set_ylabel('$\Delta$ cutting probability', fontsize=12)
ax[0].set_title('Heptamer', loc='left')
ax[0].set_title('Spacer         ') # Spaces are ad-hoc positioning
ax[0].set_title('Nonamer', loc='right')
ax[0].spines['left'].set_visible(False)
ax[1].spines['left'].set_visible(False)

df_post = cut_posts.loc[cut_posts['mutant'].isin(posterior_list)]

sort_index = dict(zip(posterior_list, range(len(posterior_list))))
df_post['rank_index'] = df_post['mutant'].map(sort_index)
df_post.sort_values(['rank_index', 'probability'], ascending=True, inplace=True)
df_post.drop('rank_index', 1, inplace=True)

for mut, mut_posts in df_post.groupby('mutant'):
        ax[2].fill_between(mut_posts['probability'] , plot_offset[mut],
                        mut_posts['posterior'] + plot_offset[mut],
                        color=post_colors[mut], alpha=0.75, zorder=post_zorder[mut])
        ax[2].plot(mut_posts['probability'], mut_posts['posterior'] + plot_offset[mut],
                        color='white', zorder=post_zorder[mut])
        ax[2].axhline(plot_offset[mut], 0, 1.0, color=post_colors[mut], alpha=1.0, zorder=post_zorder[mut])
        if mut=='WT12rss':
                text = 'reference'
        else:
                text = mut
        ax[2].text(0.95 - posterior_shift[mut], plot_offset[mut], text, backgroundcolor='#ffffff', 
                fontsize=10, color=post_colors[mut], ha="right", va="center",
                zorder=post_zorder[mut] + 1)
ax[2].set_facecolor('white')
ax[2].set_xlabel('probability of cutting')
ax[2].set_ylim([-0.025, 0.26])
ax[2].set_xlim([0.0, 1.0])
ax[2].set_yticklabels([])

# Try adding an annotation. THis may be tricky.
ax[2].vlines(0.51,plot_offset['WT12rss'], plot_offset['WT12rss'] + 0.06, color='k')
ax[2].hlines(plot_offset['WT12rss'] + 0.06, 0.49, 0.51, color='k')
ax[2].hlines(plot_offset['WT12rss'], 0.49, 0.51, color='k')
ax[2].text(0.512, plot_offset['WT12rss'] + 0.03 ,'$\propto$ probability')

# Add Figure Panels. 
fig.text(0.005, 0.9, '(A)')
fig.text(0.005, .6, '(B)')
fig.text(0.005, .35, '(C)')
plt.savefig('./point_mutation_stickplot.pdf', facecolor='white', bbox_inches='tight')




#%%

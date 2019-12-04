import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_context('talk', font_scale=1.4)


def get_plots(path, kpis):
    """
    Create plots to compare the different control strategies based on their KPIs.

    :param path: Path where the plots shall be saved in.
    :type path: str
    :param kpis: Assumption keys.
    :type kpis: list
    """
    kpis = [kpi.replace('_OPT', '') for kpi in kpis]
    stats_list = []

    for f in os.listdir(path + 'indicators/'):
        if 'indicators' in f and 'res_' not in f:
            stats = pd.read_csv('%s/%s' % (path + 'indicators/', f), index_col=0)
            stats = stats.T
            stats.columns = stats.columns.str.replace('_UC', '')
            stats.columns = stats.columns.str.replace('_DF', '')
            stats.columns = stats.columns.str.replace('_FCFS', '')
            stats.columns = stats.columns.str.replace('_WS', '')
            stats.columns = stats.columns.str.replace('_OPT', '')
            stats['evs'] = f.split('_')[1]
            stats['kW'] = f.split('_')[2]
            stats['charging_points_nr'] = f.split('_')[3]
            stats['strategy'] = f.split('_')[4]
            stats['Batt.'] = f.split('_')[6].replace('.csv', '')
            stats.loc[stats['Batt.'] == 'None', 'Batt.'] = None
            stats['Batt.'] = stats['Batt.'].astype(float)
            stats_list.append(stats)
    stats_s2 = pd.concat(stats_list, sort=False)
    stats_s2.index = range(stats_s2.shape[0])
    stats_s2.strategy = stats_s2.strategy.str.replace('UC', 'Uncontrolled')
    stats_s2.strategy = stats_s2.strategy.str.replace('DF', 'Discrimination Free')
    stats_s2.strategy = stats_s2.strategy.str.replace('FCFS', 'First Come, First Served')
    stats_s2.strategy = stats_s2.strategy.str.replace('WS', 'With Battery')
    stats_s2.strategy = stats_s2.strategy.str.replace('OPT', 'Optimized')

    for kpi in kpis:
        g = sns.catplot(data=stats_s2, y=kpi, x='kW', hue='strategy',
                        hue_order=['Uncontrolled', 'Discrimination Free', 'First Come, First Served', 'With Battery',
                                   'Optimized'
                                   ],
                        col='charging_points_nr', row='evs', kind='bar', margin_titles=True, height=6, aspect=1)

        plt.savefig(path + '/plots/' + r'%s.png' % kpi)
        plt.close('all')

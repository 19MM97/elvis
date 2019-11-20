# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
from kneed import DataGenerator, KneeLocator
from createPlot import create_plots 

# %matplotlib inline
sns.set_context("talk", font_scale=1.4)


def calc_gzf_var1(n, load="3.7"):
    if load == "3.7":
        return 0.367 + (1-0.367) / (n**0.61)
    elif load == "11":
        return 0.202 + (1-0.202) / (n**0.69)
    else:
        return 0.125 + (1-0.125) / (n**0.78)
    
def calc_gzf_var2(n, load="3.7"):
    if load == "3.7":
        return 0.367 + (1-0.367) * math.exp( -0.08 * n)
    elif load == "11":
        return 0.202 + (1-0.202) * math.exp( -0.11 * n)
    else:
        return 0.125 + (1-0.125) * math.exp( -0.15 * n)
    


s2_kpis=["Trafo Spitzenlast (%)", "Max. Gleichzeitigkeitsfaktor", "F1: Fzg.- Auslastung (%)", "F2: Energ. Auslastung (%)", "F3: Zeitl. Auslastung (%)", "Unbed. Fzg."]

stats_list = []

input_path = os.path.join(os.path.dirname(__file__),  '0_Price_1_CO2')
output_path = os.path.join(os.path.dirname(__file__), '0_Price_1_CO2_Graphs')


path = input_path #"//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/S2/Analysis_S2_16092019"
for f in os.listdir(path):
    if ("indicators" in f) and (not "res_" in f):
        stats = pd.read_csv("%s/%s" % (path, f), index_col=0)
        stats = stats.T
        stats.columns = stats.columns.str.replace("_FD", "")
        stats.columns = stats.columns.str.replace("_FCFS", "")
        stats.columns = stats.columns.str.replace("_UC", "")
        stats.columns = stats.columns.str.replace("_WS", "")
        stats.columns = stats.columns.str.replace("_OPT", "")
        stats["Fzg"] = f.split("_")[1]
        stats["kW"] = f.split("_")[2]
        stats["Anz"] = f.split("_")[3]
        stats["Strategie"] = f.split("_")[4]
        stats["Batt."] = f.split("_")[5].replace(".csv", "")
        # stats.loc[stats["Batt."] == "None", "Batt."] = None
        # print(stats["Batt."])
        # stats["Batt."] = stats["Batt."].astype(float)
        print(stats["Batt."])
        stats_list.append(stats)

stats_s2 = pd.concat(stats_list)
stats_s2.index = range(stats_s2.shape[0])
stats_s2.Strategie = stats_s2.Strategie.str.replace("UC", "Ungesteuert")
stats_s2.Strategie = stats_s2.Strategie.str.replace("WS", "Mit Batterie")
stats_s2.Strategie = stats_s2.Strategie.str.replace("FCFS", "First Come, First Served")
stats_s2.Strategie = stats_s2.Strategie.str.replace("FD", "Diskreminierungsfrei")
stats_s2.Strategie = stats_s2.Strategie.str.replace("OPT", "Optimiert(CO2)")
stats_s2["Unbed. Fzg."] = stats_s2["Angek. Fzg."] - stats_s2["Gelad. Fzg."]

stats_s2 = stats_s2.rename(columns={"F1_Fzg.- Auslastung (%)" : "F1: Fzg.- Auslastung (%)",
                                    "F2_Energ. Auslastung(%)" : "F2: Energ. Auslastung (%)", 
                                    "F3_Zeitl. Auslastung (%)" : "F3: Zeitl. Auslastung (%)" })


for kpi in s2_kpis:
    g = sns.catplot(data=stats_s2,y=kpi, x="kW", hue="Strategie", hue_order=["Ungesteuert", "First Come, First Served", "Diskreminierungsfrei", "Mit Batterie", 'Optimiert(CO2)'], col="Anz", row="Fzg", kind="bar", margin_titles=True, height=6)
    if kpi == "F1: Fzg.- Auslastung (%)":
        plt.ylim(95, 100)
    plt.savefig(output_path + "%s.png" % kpi.replace(":", ""))
    # "//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/graphs_S2/S2_"
    
lp_list = []
path = input_path#"//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/S2/Analysis_S2_16092019"
for f in os.listdir(path):
    if "LoadProfile" in f:
        load = pd.read_csv("%s/%s" % (path, f), index_col=0, parse_dates=[0])
        load = load.LP_total_load_kW
        lp_list.append(load)
load_s2 = pd.concat(lp_list, axis=1)
load_s2.columns = range(load_s2.shape[1])
load_s2["minuteofweek"] = (load_s2.index.dayofweek) * 24 * 60 + (load_s2.index.hour) * 60  + load_s2.index.minute
load_s2["hourofweek"] = (load_s2.index.dayofweek) * 24 + (load_s2.index.hour)
load_s2["15min_interval"] = (load_s2.index.dayofweek) * 24 * 4 + (load_s2.index.hour) * 4  + load_s2.index.minute // 15
load_s2.head()
#
## plot the first week
#for anz in [20., 30.]:
#    for fzg in [225, 550]:
#        df_tmp = stats_s2.loc[(stats_s2["Fzg"] =="%d" % fzg) & (stats_s2["Anz"] =="%d" % anz) & (stats_s2["Strategy"] =="UC") & stats_s2["kW"].isin(["11","22"])]
#        labels = ["%s kW" % l for l in df_tmp["kW"].values.tolist()[::-1]]
#        idx =df_tmp.index[::-1]
#
#        ax = load_s2.iloc[:60*24*7,idx].plot(figsize=(16,8))
#        legend1 = ax.legend(labels, loc="upper right")
#        ax.axhline(y=calc_gzf_var1(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="--")
#        ax.axhline(y=calc_gzf_var1(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls="--")
#        ax.axhline(y=calc_gzf_var2(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls=":")
#        ax.axhline(y=calc_gzf_var2(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls=":")
#        ax.axhline(y=0.33 * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="-.")
#
#        legend_elements = [Line2D([0], [0], color='black', lw=2, label='Rohlink 2013 Var. 1', ls="--"),
#                           Line2D([0], [0], color='black', lw=2, label='Rohlink 2013 Var. 2', ls=":"),
#                           Line2D([0], [0], color='black', lw=2, label='VBEW 2018', ls="-.")]
#        legend2 = ax.legend(handles=legend_elements, loc="upper left")
#        ax.add_artist(legend1)
#        ax.add_artist(legend2)
#
#        ax.set_xlabel("")
#        ax.set_title("Bsp. Wochenlastgang in Minuten-Auflösung (%s LP, %s Fzg./Woche)" % (anz, fzg))
#        sns.despine()
#        plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/graphs_S2/%s_firstweek_with_gzf_minutly_%s_%s.png" % ("S2", anz, fzg)) 
#
## plot the first week
#for anz in [20., 30.]:
#    for fzg in [225, 550]:
#        df_tmp = stats_s2.loc[(stats_s2["Fzg"] =="%d" % fzg) & (stats_s2["Anz"] =="%d" % anz) & (stats_s2["Strategy"] =="UC") & stats_s2["kW"].isin(["11","22"])]
#        labels = ["%s kW" % l for l in df_tmp["kW"].values.tolist()[::-1]]
#        idx =df_tmp.index[::-1]
#
#        ax = load_s2.iloc[:60*24*7,idx].resample("15min").mean().plot(figsize=(16,8))
#        legend1 = ax.legend(labels, loc="upper right")
#        ax.axhline(y=calc_gzf_var1(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="--")
#        ax.axhline(y=calc_gzf_var1(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls="--")
#        ax.axhline(y=calc_gzf_var2(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls=":")
#        ax.axhline(y=calc_gzf_var2(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls=":")
#        ax.axhline(y=0.33 * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="-.")
#
#        legend_elements = [Line2D([0], [0], color='black', lw=2, label='Rohlink 2013 Var. 1', ls="--"),
#                           Line2D([0], [0], color='black', lw=2, label='Rohlink 2013 Var. 2', ls=":"),
#                           Line2D([0], [0], color='black', lw=2, label='VBEW 2018', ls="-.")]
#        legend2 = ax.legend(handles=legend_elements, loc="upper left")
#        ax.add_artist(legend1)
#        ax.add_artist(legend2)
#
#        ax.set_xlabel("")
#        ax.set_title("Bsp. Wochenlastgang in 15 Minuten-Auflösung (%s LP, %s Fzg./Woche)" % (anz, fzg))
#        sns.despine()
#        plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/graphs_S2/%s_firstweek_with_gzf_15min_%s_%s.png" % ("S2", anz, fzg)) 
#        
#
#for anz in [20., 30.]:
#    for fzg in [225, 550]:
#        df_tmp = stats_s2.loc[(stats_s2["Fzg"] =="%d" % fzg) & (stats_s2["Anz"] =="%d" % anz) & (stats_s2["Strategy"] == "UC") & stats_s2["kW"].isin(["11","22"])]
#        labels = ["%s kW" % l for l in df_tmp["kW"].values.tolist()[::-1]]
#        idx =df_tmp.index[::-1]
#
#        # 15 minute dauerkennline
#        fig, ax = plt.subplots(1,1, figsize=(16,8))
#        for i in idx:
#            df_dauerkennlinie = load_s2.loc[:,[i]].resample("15min").mean().sort_values(by=i, ascending=False)
#            df_dauerkennlinie.index = range(load_s2.loc[:,idx.tolist()].resample("15min").mean().shape[0])
#            df_dauerkennlinie.plot(ax=ax)
#        legend1 = ax.legend(labels, loc="upper right")
#        ax.axhline(y=calc_gzf_var1(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="--")
#        ax.axhline(y=calc_gzf_var1(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls="--")
#        ax.axhline(y=calc_gzf_var2(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls=":")
#        ax.axhline(y=calc_gzf_var2(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls=":")
#        ax.axhline(y=0.33 * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="-.")
#
#        legend_elements = [Line2D([0], [0], color='black', lw=2, label='Rohlink 2013 Var. 1', ls="--"),
#                           Line2D([0], [0], color='black', lw=2, label='Rohlink 2013 Var. 2', ls=":"),
#                           Line2D([0], [0], color='black', lw=2, label='VBEW 2018', ls="-.")]
#        legend2 = ax.legend(handles=legend_elements, loc="upper left")
#        ax.add_artist(legend1)
#        ax.add_artist(legend2)
#        ax.set_title("Dauerkennlinie in 15-Minuten-Auflösung (%d LP, %s Fzg./Woche)" % (anz, fzg))
#        sns.despine()
#        plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/graphs_S2/kennlinie_15min_%s_%s.png" % (anz, fzg)) 
#        
#for anz in [20., 30.]:
#    for fzg in [225, 550]:
#        df_tmp = stats_s2.loc[(stats_s2["Fzg"] =="%d" % fzg) & (stats_s2["Anz"] =="%d" % anz) & (stats_s2["Strategy"] == "UC") & stats_s2["kW"].isin(["11","22"])]
#        labels = ["%s kW" % l for l in df_tmp["kW"].values.tolist()[::-1]]
#        idx =df_tmp.index[::-1]
#        
#        # only day
#        long_df = load_s2.loc[load_s2.index.dayofweek==0,idx.tolist() + ["hourofweek"]].resample("15min").max()
#        long_df.columns = labels + ["hourofweek"]
#        wide_df_list = []
#        for c in long_df.columns[:-1]:
#            single_df = long_df[[c, "hourofweek"]]
#            single_df.columns= ["Wert", "hourofweek"]
#            single_df.loc[:,"Kategorie"] = c
#            wide_df_list.append(single_df)
#        long_df = pd.concat(wide_df_list)
#        long_df
#
#        fig, axes = plt.subplots(1,2, figsize=(20, 8), sharey=True)
#        fig.suptitle("Verteilung von 15 Minuten Spitzenlast (%d LP, %s Fzg./Woche)" % (anz, fzg))
#        sns.boxenplot(x="hourofweek", y="Wert", data=long_df, hue="Kategorie", ax=axes[0])
#        sns.boxenplot(x="hourofweek", y="Wert", data=long_df, hue="Kategorie", ax=axes[1])
#        axes[0].set_ylabel("")
#        axes[1].set_ylabel("")
#        axes[0].set_xlabel("")
#        axes[1].set_xlabel("")
#        axes[0].set_xticklabels(range(0,24))#
#        axes[1].set_xticklabels(range(0,24))#
#        
#        legend1 = axes[0].legend(labels, loc="upper left")
#        axes[0].axhline(y=calc_gzf_var1(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="--")
#        axes[0].axhline(y=calc_gzf_var1(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls="--")
#        axes[0].axhline(y=calc_gzf_var2(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls=":")
#        axes[0].axhline(y=calc_gzf_var2(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls=":")
#        axes[0].axhline(y=0.33 * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="-.")
#        
#        axes[1].axhline(y=calc_gzf_var1(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="--")
#        axes[1].axhline(y=calc_gzf_var1(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls="--")
#        axes[1].axhline(y=calc_gzf_var2(anz, "11") * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls=":")
#        axes[1].axhline(y=calc_gzf_var2(anz, "22") * 22 * anz, xmin=0.0, xmax=1.0, color="#1f77b5", ls=":")
#        axes[1].axhline(y=0.33 * 11 * anz, xmin=0.0, xmax=1.0, color="#ff7f0e", ls="-.")
#
#        legend_elements = [Line2D([0], [0], color='black', lw=2, label='Rohlink 2013 Var. 1', ls="--"),
#                           Line2D([0], [0], color='black', lw=2, label='Rohlink 2013 Var. 2', ls=":"),
#                           Line2D([0], [0], color='black', lw=2, label='VBEW 2018', ls="-.")]
#        legend2 = axes[1].legend(handles=legend_elements, loc="upper right")
#        axes[0].add_artist(legend1)
#        axes[1].add_artist(legend2)
#       
#        plt.tight_layout()
#        sns.despine()
#        plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/graphs_S2/weekday_weekend_%s_%s.png" % (anz, fzg)) 
#        
df_tmp = stats_s2.loc[(stats_s2["Fzg"] =="550") & (stats_s2["Anz"] =="30") & (stats_s2["Strategie"] =="Ungesteuert")]
labels = df_tmp["kW"].values.tolist()
idx =df_tmp.index
create_plots(load_s2, idx[::-1], ["%s kW" % l for l in labels[::-1]], 'graphs_S2', "load")

df_tmp = stats_s2.loc[(stats_s2["kW"] =="22") & (stats_s2["Anz"] =="30") & (stats_s2["Strategie"] =="Ungesteuert")]
labels = df_tmp["Fzg"].values.tolist()
idx =df_tmp.index
create_plots(load_s2, idx[::-1], labels[::-1], "graphs_S2", "anzahl_fzg")

df_tmp = stats_s2.loc[(stats_s2["kW"] =="22") & (stats_s2["Fzg"] =="550") & (stats_s2["Strategie"] =="Ungesteuert")]
labels = df_tmp["Anz"].values.tolist()
idx =df_tmp.index
create_plots(load_s2, idx[::-1], labels[::-1], "S2", "anzahl_stationen")

df_tmp = stats_s2.loc[(stats_s2["kW"] =="22") & (stats_s2["Fzg"] =="550") & (stats_s2["Anz"] =="30")]
labels = df_tmp["Strategie"].values.tolist()
idx =df_tmp.index
create_plots(load_s2, idx[::-1], labels[::-1], "S2", "strategy")

df_tmp = stats_s2.loc[(stats_s2["kW"] =="50") & (stats_s2["Fzg"] =="550") & (stats_s2["Anz"] =="30")]
labels = df_tmp["Strategie"].values.tolist()
idx =df_tmp.index
create_plots(load_s2, idx[::-1], labels[::-1], "S2", "strategy_50")
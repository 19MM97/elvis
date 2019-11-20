from typing import List

import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math


sns.set_context("talk", font_scale=1.4)


def get_plots(path, kpis):
    kpis = [kpi.replace ("_OPT", "") for kpi in kpis]
    stats_list = []
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
            stats["Batt."] = f.split("_")[6].replace(".csv", "")
            stats.loc[stats["Batt."] == "None", "Batt."] = None
            stats["Batt."] = stats["Batt."].astype(float)
            stats_list.append(stats)
    stats_s2 = pd.concat(stats_list, sort=False)
    stats_s2.index = range(stats_s2.shape[0])
    stats_s2.Strategie = stats_s2.Strategie.str.replace("UC", "Ungesteuert")
    stats_s2.Strategie = stats_s2.Strategie.str.replace("WS", "Mit Batterie")
    stats_s2.Strategie = stats_s2.Strategie.str.replace("FCFS", "First Come, First Served")
    stats_s2.Strategie = stats_s2.Strategie.str.replace("FD", "Diskreminierungsfrei")
    stats_s2.Strategie = stats_s2.Strategie.str.replace("OPT", "Optimiert")

    for kpi in kpis:
        g = sns.catplot(data=stats_s2, y=kpi, x="kW", hue="Strategie",
                        hue_order=["Ungesteuert", "First Come, First Served", "Diskreminierungsfrei", "Mit Batterie", 'Optimiert'],
                        col="Anz", row="Fzg", kind="bar", margin_titles=True, height=6, aspect=1)

        plt.savefig(path + '%s.png' % kpi)

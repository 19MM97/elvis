import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def create_plots(load, idx, labels, path, name):
    # plot the first week
    ax = load.iloc[:60*24*7,idx].plot(figsize=(16,8))
    legend1 = ax.legend(labels, loc="upper right")
    ax.set_xlabel("Minuten")
    ax.set_ylabel ("kVA")
    ax.set_title("Bsp. Wochenlastgang in Minuten-Auflösung")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_firstweek_minute.png" % (path, name)) 
    
    # plot the first week in 15min resolution
    ax = load.iloc[:60*24*7,idx].resample("15min").mean().plot(figsize=(16,8))
    legend1 = ax.legend(labels, loc="upper right")
    ax.set_xlabel("")
    ax.set_ylabel ("kVA")
    ax.set_title("Bsp. Wochenlastgang in 15 Minuten-Auflösung")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_firstweek_15min.png" % (path, name)) 

    # plot the first week in hourly resolution
    ax = load.iloc[:60*24*7,idx].resample("H").mean().plot(figsize=(16,8))
    legend1 = ax.legend(labels, loc="upper right")
    ax.set_xlabel("")
    ax.set_ylabel ("kVA")
    ax.set_title("Bsp. Wochenlastgang in Stunden-Auflösung")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_firstweek_hourly.png" % (path, name)) 

    # plot minute averages
    df = load.loc[:,idx.tolist() + ["minuteofweek"]]
    ax = df.groupby("minuteofweek").mean().rename_axis('MinuteOfWeek').plot(figsize=(16,8))
    legend1 = ax.legend(labels, loc="upper right")
    ax.set_xlabel("")
    ax.set_ylabel ("kVA")
    ax.set_title("Durchschnittlicher Wochenlastgang in Minuten-Auflösung")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_averages_minute.png" % (path, name)) 

    # plot minute averages
    df = load.loc[:,idx.tolist() + ["hourofweek"]]
    ax = df.groupby("hourofweek").mean().rename_axis('HourOfWeek').plot(figsize=(16,8))
    legend1 = ax.legend(labels, loc="upper right")
    ax.set_xlabel("Stunden")
    ax.set_ylabel ("kVA")
    ax.set_title("Durchschnittlicher Wochenlastgang in Stunden-Auflösung")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_averages_hourly.png" % (path, name)) 
    
    # plot minute averages
    df = load.loc[:,idx.tolist() + ["15min_interval"]]
    ax = df.groupby("15min_interval").mean().rename_axis('15min Interval').plot(figsize=(16,8))
    legend1 = ax.legend(labels, loc="upper right")
    ax.set_title("Durchschnittlicher Wochenlastgang in 15 Minuten-Auflösung")
    ax.set_xlabel("")
    ax.set_ylabel ("kVA")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_averages_15min.png" % (path, name)) 

    # boxplot
    fig, axes = plt.subplots(len(idx),1, figsize=(20, 20), sharey=True)
#    fig.subtitle("Verteilung von 15 Minuten Spitzenlast")
    for j, i in enumerate(idx):
        sns.boxenplot(x="hourofweek", y=i, data=load.loc[:,[i,"hourofweek"]].resample("15min").max(), ax=axes[j], color="royalblue", label=labels[j])
        axes[j].set_title("%s kW" % labels[j])
        axes[j].set_xlabel("Viertelstunden")
        axes[j].set_ylabel("kVA")
        axes[j].set_xticks(range(0,169,6))
        axes[j].set_xticklabels(range(0,169,6))#
        sns.despine(offset=10, trim=True)
    plt.tight_layout()
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_boxplot_week_15min_max.png" % (path, name)) 

    # only day
    long_df = load.loc[load.index.dayofweek==0,idx.tolist() + ["hourofweek"]].resample("15min").max()
    long_df.columns = labels + ["hourofweek"]
    wide_df_list = []
    for c in long_df.columns[:-1]:
        single_df = long_df[[c, "hourofweek"]]
        single_df.columns= ["Wert", "hourofweek"]
        single_df.loc[:,"Kategorie"] = c
        wide_df_list.append(single_df)
    long_df = pd.concat(wide_df_list)
    long_df

    fig, axes = plt.subplots(1,2, figsize=(20, 8), sharey=True)
    fig.suptitle("Verteilung von 15 Minuten Spitzenlast")
    sns.boxenplot(x="hourofweek", y="Wert", data=long_df, hue="Kategorie", ax=axes[0])
    sns.boxenplot(x="hourofweek", y="Wert", data=long_df, hue="Kategorie", ax=axes[1])
    axes[0].set_ylabel("kVA")
    axes[1].set_ylabel("kVA")
    axes[0].set_xlabel("Viertelstunden")
    axes[1].set_xlabel("Viertelstunden")
    axes[0].set_xticklabels(range(0,24))#
    axes[1].set_xticklabels(range(0,24))#
    plt.tight_layout()
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_weekday_weekend.png" % (path, name)) 


    # minue dauerkennline
    fig, ax = plt.subplots(1,1, figsize=(16,8))
    for i in idx:
        df_dauerkennlinie = load.loc[:,[i]].sort_values(by=i, ascending=False)
        df_dauerkennlinie.index = range(load.loc[:,idx.tolist()].shape[0])
        df_dauerkennlinie.plot(ax=ax)
    ax.legend(labels)
    ax.set_title("Dauerkennlinie in Minutenauflösung")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_kennlinie_minute.png" % (path, name)) 
    
    # 15 minute dauerkennline
    fig, ax = plt.subplots(1,1, figsize=(16,8))
    for i in idx:
        df_dauerkennlinie = load.loc[:,[i]].resample("15min").mean().sort_values(by=i, ascending=False)
        df_dauerkennlinie.index = range(load.loc[:,idx.tolist()].resample("15min").mean().shape[0])
        df_dauerkennlinie.plot(ax=ax)
    legend1 = ax.legend(labels, loc="upper right")
    ax.set_title("Dauerkennlinie in 15-Minuten-Auflösung")
    ax.set_ylabel("kVA")
    ax.set_xlabel("Viertelstunden")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_kennlinie_15min.png" % (path, name)) 

    # hour dauerkennline
    fig, ax = plt.subplots(1,1, figsize=(16,8))
    for i in idx:
        df_dauerkennlinie = load.loc[:,[i]].resample("H").mean().sort_values(by=i, ascending=False)
        df_dauerkennlinie.index = range(load.loc[:,idx.tolist()].resample("H").mean().shape[0])
        df_dauerkennlinie.plot(ax=ax)
    legend1 = ax.legend(labels, loc="upper right")
    ax.set_title("Dauerkennlinie in Stunden-Auflösung")
    ax.set_ylabel("kVA")
    ax.set_xlabel("Viertelstunden")
    sns.despine()
    plt.savefig("//dainas/ac/Energy/Projects/2017/FlexNet4E/docs/Deliverables/simulation results/simulation analysis/%s/%s_kennlinie_hour.png" % (path, name)) 
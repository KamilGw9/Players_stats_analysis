import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/kamil/Desktop/S2324-laliga-players.csv')
pd.set_option('display.max_columns', 150)
print(df.head(5))

column_names = df.columns.tolist()
print(column_names)

df = df[['competition', 'name', 'team', 'position', 'aerial_duels', 'aerial_duels_lost', 'aerial_duels_won',
         'assists_intentional', 'blocks', 'duels', 'duels_lost', 'duels_won', 'goal_assists', 'goal_kicks', 'goals',
         'goals_from_inside_box', 'goals_from_outside_box', 'ground_duels', 'ground_duels_lost', 'ground_duels_won',
         'headed_goals', 'interceptions', 'key_passes_attempt_assists', 'second_goal_assists',
         'shots_off_target_inc_woodwork', 'shots_on_target_inc_goals', 'successful_dribbles', 'successful_long_passes',
         'successful_crosses_open_play', 'successful_short_passes', 'time_played', 'total_clearances',
         'total_losses_of_possession', 'total_passes', 'total_shots', 'total_touches_in_opposition_box', 'touches',
         'unsuccessful_crosses_open_play', 'unsuccessful_dribbles', 'unsuccessful_long_passes',
         'unsuccessful_short_passes', 'winning_goal']]
print(df)

print(df.info())
print(df.isna().sum())
df = df.dropna(subset=['team', 'position'])
df = df.fillna(0)
print(df.isna().sum())

float_columns = df.select_dtypes(include=['float64']).columns
df[float_columns] = df[float_columns].astype(int)
print(df.info())

df = df[df['competition'] == 'Classics']
df = df[df['position'] != 'Goalkeeper']
df = df[
    ~df['team'].isin(['CD Leganés', 'CD Mirandés', 'Real Valladolid CF', 'Real Zaragoza', 'SD Huesca', 'Villarreal B'])]
df = df[df['time_played'] >= 800]
df = df.reset_index(drop=True)
print(df)


def add_win_percent(df, win_column, loss_column, new_column):
    win_percent = (df[win_column] / (df[win_column] + df[loss_column])) * 100
    win_percent = round(win_percent, 0)
    df.loc[:, new_column] = win_percent


def per90(df, first_value, timeplayed, new_col):
    value_90 = (df[first_value] / df[timeplayed]) * 90
    value_90 = round(value_90, 2)
    df.loc[:, new_col] = value_90


add_win_percent(df, 'duels_won', 'duels_lost', 'Duels')
add_win_percent(df, 'aerial_duels_won', 'aerial_duels_lost', 'Aerial duels')
add_win_percent(df, 'successful_dribbles', 'unsuccessful_dribbles', 'Dribbles')
add_win_percent(df, 'successful_short_passes', 'unsuccessful_short_passes', 'Short passes')
add_win_percent(df, 'successful_long_passes', 'unsuccessful_long_passes', 'Long passes')
add_win_percent(df, 'successful_crosses_open_play', 'unsuccessful_crosses_open_play', 'Open play crosses')

print(df)

per90(df, 'interceptions', 'time_played', 'Interception')
per90(df, 'total_touches_in_opposition_box', 'time_played', 'Touches in box')
per90(df, 'total_shots', 'time_played', 'Total shots')
per90(df, 'shots_on_target_inc_goals', 'time_played', 'Shots on target inc goals')
per90(df, 'shots_off_target_inc_woodwork', 'time_played', 'Shots off target inc woodwork')
per90(df, 'second_goal_assists', 'time_played', 'Second goal assist')
per90(df, 'goal_assists', 'time_played', 'Goal Assist')
per90(df, 'goals', 'time_played', 'Goals')
per90(df, 'blocks', 'time_played', 'Blocks')
per90(df, 'total_clearances', 'time_played', 'Clearances')
per90(df, 'key_passes_attempt_assists', 'time_played', 'Key passes attempt')

print(df)


def show_stats(df, name_player):
    columns90 = (
    'Interception', 'Touches in box', 'Total shots', 'Shots on target inc goals', 'Shots off target inc woodwork',
    'Second goal assist', 'Goal Assist', 'Goals', 'Key passes attempt', 'Blocks', 'Clearances')
    column = ('Duels', 'Aerial duels', 'Dribbles', 'Short passes', 'Long passes', 'Open play crosses')

    if name_player not in df['name'].values:
        print('Player doesnt exist')
        return

    player_row = df[df['name'] == name_player]

    stats_values = []
    stats_labels = []

    for col in columns90:
        if col in player_row.columns:
            stats_values.append(player_row[col].values[0])
            stats_labels.append(col)
        else:
            print(f"Nie znaleziono kolumny: {col}")

    fig, ax1 = plt.subplots()
    plt.xticks(rotation=90)
    plt.xticks(fontsize=10)

    bars = ax1.bar(stats_labels, stats_values, color='skyblue')
    ax1.set_ylabel('Values per 90 minutes', color='black', fontsize=12)

    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom', ha='center', fontsize=8)

    ax2 = ax1.twinx()

    player_row = df[df['name'] == name_player]

    stats_values = []
    stats_labels = []

    for col in column:
        if col in player_row.columns:
            stats_values.append(player_row[col].values[0])
            stats_labels.append(col)
        else:
            print(f"Nie znaleziono kolumny: {col}")

    bars = ax2.bar(stats_labels, stats_values, color='green', alpha=0.5)
    ax2.set_ylabel('Success rate %', color='black', fontsize=12)
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom', ha='center', fontsize=8)

    plt.title(f"Player Stats: {name_player}")
    ax1.grid(False)
    ax2.grid(False)
    plt.show()


correlation = df['Key passes attempt'].corr(df['Goal Assist'])
print(correlation)

top_assist = df.nlargest(10, 'Goal Assist')['name']
selected_players = top_assist.tolist()
print(selected_players)

plt.figure(figsize=(10, 8))

for player in selected_players:
    player_data = df[df['name'] == player]

    plt.scatter(player_data['Key passes attempt'], player_data['Goal Assist'], label=player)

plt.legend()
plt.title('Relation between Key passes attempt and assists per 90')
plt.xlabel('Key Passes Attempt')
plt.ylabel('Assists')

plt.grid(True)

plt.show()

show_stats(df, 'Raphael Dias Belloli'), show_stats(df, 'Álex Baena'), show_stats(df, 'Toni Kroos')

correlation = df['Total shots'].corr(df['Goals'])
print(correlation)

top_goals = df.nlargest(10, 'Goals')['name']
selected_players3 = top_goals.tolist()
print(top_goals.tolist())

plt.figure(figsize=(10, 8))

for player in selected_players3:
    player_data = df[df['name'] == player]

    plt.scatter(player_data['Goals'], player_data['Total shots'], label=player)

plt.legend()
plt.title('Relation between Total shots and Goals per 90')
plt.xlabel('Goals')
plt.ylabel('Total shots')

plt.grid(True)
plt.show()

show_stats(df, 'Jude Bellingham'), show_stats(df, 'Álvaro Morata'), show_stats(df, 'Ángel Correa')
print(df)

df_summary1 = df.groupby('team')['goals_from_outside_box'].mean()
df_summary2 = df.groupby('team')['goals_from_inside_box'].mean()
df_summary3 = df.groupby('team')['Duels'].mean()
df_summary4 = df.groupby('team')['total_passes'].mean()
df_summary5 = df.groupby('team')['Short passes'].mean()
df_summary6 = df.groupby('team')['Long passes'].mean()


def mean_axhline(mean_value, summary_df):
    plt.axhline(mean_value, color='blue', label=f'Average : {mean_value:.2f}')
    for i, value in enumerate(summary_df):
        if value > mean_value:
            plt.gca().get_children()[i].set_color('green')
        else:
            plt.gca().get_children()[i].set_color('red')
    plt.legend()


plt.figure(figsize=(20, 8))
plt.subplot(1, 3, 1)
plt.title('Total passes')
sns.barplot(x=df_summary4.index, y=df_summary4, )
plt.ylabel('Team mean value')
plt.xticks(rotation=90)
plt.xticks(fontsize=10)
mean_value = df_summary4.mean()
mean_axhline(mean_value, df_summary4)

plt.subplot(1, 3, 2)
plt.title('Goals from outside box')
sns.barplot(x=df_summary1.index, y=df_summary1, )
plt.ylabel('Values per 90')
plt.xticks(rotation=90)
plt.xticks(fontsize=10)
mean_value = df_summary1.mean()
mean_axhline(mean_value, df_summary1)

plt.subplot(1, 3, 3)
plt.title('Goals from inside box')
sns.barplot(x=df_summary2.index, y=df_summary2, )
plt.ylabel('Values per 90')
plt.xticks(rotation=90)
plt.xticks(fontsize=10)
mean_value = df_summary2.mean()
mean_axhline(mean_value, df_summary2)

plt.tight_layout()
plt.legend()
plt.show()

plt.figure(figsize=(20, 8))
plt.subplot(1, 3, 1)
plt.title('Average duels won per team')
sns.barplot(x=df_summary3.index, y=df_summary3, )
plt.ylabel('Success rate %')
plt.xticks(rotation=90)
plt.xticks(fontsize=10)
mean_value = df_summary3.mean()
mean_axhline(mean_value, df_summary3)

plt.subplot(1, 3, 2)
plt.title('Short passes')
sns.barplot(x=df_summary5.index, y=df_summary5, )
plt.ylabel('Success rate %')
plt.xticks(rotation=90)
plt.xticks(fontsize=10)
mean_value = df_summary5.mean()
mean_axhline(mean_value, df_summary5)

plt.subplot(1, 3, 3)
plt.title('Long passes ')
sns.barplot(x=df_summary6.index, y=df_summary6, )
plt.ylabel('Success rate %')
plt.xticks(rotation=90)
plt.xticks(fontsize=10)
mean_value = df_summary6.mean()
mean_axhline(mean_value, df_summary6)

plt.tight_layout()
plt.legend()
plt.show()







import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from PIL import Image

# image = Image.open('/Users/aniruddhbhaskaran/Programming/Python/Data_Analysis/teahub.io-golden-state-warriors-wallpaper-109704.png')
# st.image(image)

st.title("Golden State Warriors 2020-21 Season Analytics Project")

st.header("By Aniruddh Bhaskaran (Ashoka University UG '23)")

st.subheader("Date: 14th May 2021")

# read data into the dashboard - cleaned data sourced from warriors.ipynb
roster = pd.read_csv('https://raw.githubusercontent.com/LaserTrajectory/gsw-dash/main/roster.csv')
per_game = pd.read_csv('https://raw.githubusercontent.com/LaserTrajectory/gsw-dash/main/per_game.csv')
totals = pd.read_csv('https://raw.githubusercontent.com/LaserTrajectory/gsw-dash/main/totals.csv')
per_36_min = pd.read_csv('https://raw.githubusercontent.com/LaserTrajectory/gsw-dash/main/per_36_min.csv')
per_100_poss = pd.read_csv('https://raw.githubusercontent.com/LaserTrajectory/gsw-dash/main/per_100_poss.csv')
advanced = pd.read_csv('https://raw.githubusercontent.com/LaserTrajectory/gsw-dash/main/advanced.csv')
win_loss_clean = pd.read_csv('https://raw.githubusercontent.com/LaserTrajectory/gsw-dash/main/win_loss_clean_excel_test_2.csv')
# win_loss_cols = game_log[["G", "Date", "Opp", "W/L", "Tm", "Opp"]]

# win_loss = win_loss_cols.copy()

# any further cleaning that needs to be done can be done here
roster.drop(columns=["Unnamed: 0"], inplace=True)
# win_loss_clean.drop(columns=["Table 1"], inplace=True)
win_loss_clean.rename(columns={"Unnamed: 1":"Date", "Unnamed: 2":"Opp", "Unnamed: 3":"W/L", "Tm":"Team Score", "Opp.1":"Opp Score"}, inplace=True)
new_w_l = win_loss_clean.copy()
new_w_l.index = list(range(1, 71))
new_w_l['Point Differential'] = new_w_l['Team Score'] - new_w_l['Opp Score']
avg_pt_diff = new_w_l["Point Differential"].mean()
per_game.drop(columns=["Unnamed: 0"], inplace=True)
per_game.index = list(range(1, 18))
per_100_poss.drop(columns=["Unnamed: 0"], inplace=True)
per_100_poss.index = list(range(1, 18))
advanced.drop(columns=["Unnamed: 0"], inplace=True)
advanced.index = list(range(1, 18))


st.markdown("This dashboard utilises data from basketballreference.com and some Python modules to give a analytical overview of the Warriors 2020-21 season, and provide some inferences.")

st.markdown("All data is scraped/sourced from https://www.basketball-reference.com/teams/GSW/2021.html.")

st.write("=========================================================================")

st.sidebar.title("Visualisations")
st.sidebar.markdown("Choose from the options below to get an overview of the data: ")

viz_select = st.sidebar.selectbox('Data', ('Season Overview', 'Roster', 'Per Game', 'Per 100 Possessions', 'Advanced'))

if viz_select == "Season Overview":

    st.sidebar.write("""The Season Overview tab provides information on the overall trends
    through the season for the Warriors, including win-loss trends and point differentials.""")

    st.header("GSW 2020-21 Season Overview")

    st.write(new_w_l)

    st.write("The average point differential for the Warriors this season is ", avg_pt_diff, ".")

    st.write("This tells us that while they have won more than they've lost, on average, they don't win by much.")

    st.write("The Warriors record this season: ")

    w_l_count = new_w_l['W/L'].value_counts()

    st.write(w_l_count)

    # fig = go.Figure(data=[
    #     go.Bar(name='GSW', x=new_w_l['Date'][1:10], y=new_w_l['Team Score'][1:10]),
    #     go.Bar(name='Opp', x=new_w_l['Date'][1:10], y=new_w_l['Opp Score'][1:10])
    # ])

    # fig.update_layout(barmode='group')

    # fig.update_layout(
    #     hoverlabel=dict(
    #         bgcolor="white",
    #         font_size=16,
    #         font_family="Rockwell"
    #     )
    # )

    fig = px.scatter(new_w_l, x="Team Score", y="Opp Score", 
                    color="W/L", hover_data=["Date", "Point Differential"],
                    color_discrete_map={"W":"green", "L":"red"}, 
                    title="Team Score vs. Opponent Score: Sorted by Win/Loss",
                    hover_name="Opp")

    st.plotly_chart(fig)

    st.write("""We can see from the graph above that there seems to be a higher number of losses 
    when the opponent scores a higher number of points. When opponents score greater than 120 points,
    the Warriors generally lose that game – and by quite a bit. Most of the losses are clustered
    in the area where the Warriors' team score is around a 100, and opponents score in the 110-
    130 range.""")

    st.write("""This could indicate that the Warriors are either unable to keep production or stamina up
    towards the end of the game, or that once their opponent has a lead on them, they are unable to go
    on runs and make a comeback.""")

    fig_2 = px.scatter(new_w_l, x="Opp", y="Point Differential", color="W/L",
                       title="Opponent vs. Point Differential: Sorted by Win/Loss", 
                       hover_data=["Date"], color_discrete_map={"W":"green", "L":"red"})

    st.plotly_chart(fig_2)

    st.write("""This chart shows us that the point differential per opponent, sorted by wins and losses.
    We see that the Warriors have games where they have won by large margins (20+) but also lost by
    significant margins. Many playoff teams such as Brooklyn, Milwaukee, the LA Lakers and Clippers, Dallas,
    Phoenix and Utah have beaten the Warriors by margins around 20 or above.""") 
    
    st.write("""What's worrisome, however, is that
    teams that are not in the playoff hunt have also managed to blow out the Warriors. The Warriors have played Sacramento
    twice, with one loss and one win. However the point differential in the win was just 4, while the point 
    differential in the loss was -22. We can chalk such games up to injuries to players like Steph Curry and Kelly Oubre, but it
    shows that the bench needs to improve if the Warriors are to succeed come play-in tournament (and 
    hopefully playoff) time.""")

if viz_select == "Roster":

    st.sidebar.write("""The Roster tab provides information on the players themselves,
    including height, weight, country of origin, and position played.""")

    st.header("GSW 2020-21 Roster")
    st.dataframe(roster)

    ht_wt = px.scatter(roster, x="Ht", y="Wt", color="Pos", 
    hover_data=["Player"], title="Players' Height by Weight: Sorted by Position")

    st.plotly_chart(ht_wt)

    origin = st.checkbox("Show countries of origin for players")

    if origin:

        countries = px.pie(roster, names='POB', title="Countries of Origin")

        countries.update_traces(textinfo='value')

        st.plotly_chart(countries)

    position = st.checkbox("Show number of players per position")

    if position:

        pos = px.pie(roster, names='Pos', title="Number of Players per Position")

        pos.update_traces(textinfo='value')

        st.plotly_chart(pos)

if viz_select == "Per Game":

    st.sidebar.write("""The Per Game tab provides analyses based on the Per Game average
    for each player on the Warriors team.""")

    st.header("GSW 2020-21 Per Game Stats")

    per_game_hm = per_game.style.background_gradient(cmap='viridis')

    st.write(per_game_hm)

    st.write("""The data frame above is formatted based on which values are outliers compared to the average
    over the range of values that each column takes. This helps to quickly identify statistical outliers,
    especially among those who are lower down in the table. One such example is the fact that Kevon Looney
    grabs 1.9 Offensive Rebounds per Game, while being only 10th in minutes played. This shows us that
    Looney is a important player to have on the court, especially down the stretch when baskets are needed.
    Offensive rebounding gives teams a second chance to score, and therefore those who have an affinity
    for getting them are vital to the team. """)

    st.header("Per Game Analytics and Inferences")

    st.subheader("Longevity and Consistency")

    game_mins = px.scatter(per_game, x="G", y="MP", size="PTS/G", hover_data=["Name", "Age"], 
                title="Games Played vs. Minutes per Game Played with Size = Points per Game")

    st.plotly_chart(game_mins)

    st.write("""The chart below shows the number of games played vs. the minutes played per game, and each
    point is sized according the point per game scored by each played. We see immediately that Steph Curry's
    bubble is the biggest – he is currently averaging 31.8 points per game, which leads both his team
    and the entire league. The player with the second highest points per game on the Warriors is Andrew 
    Wiggins, with 18.6 PPG. This is not extremely high, but Andrew is the only Warrior who has played
    every game so far this season – his longevity and reliability is something that few other Warriors 
    have had this season.""")

    st.write("""In fact, only 4 Warriors have played 60 or more games this season, as can be seen from the
    graph – Curry, Green, Wiggins and Bazemore. And only 4 Warriors average more than 30 minutes per game –
    Oubre, Curry, Green and Wiggins. Injuries have plagued the Warriors this season, which is why it is 
    vital that the Warriors bench steps up, especially in crunch time.""")

    st.subheader("Efficient Offensive Production")

    min_shots = px.scatter(per_game, x="MP", y="FG%", size="eFG%", hover_data=["G", "PTS/G", "3P%", "3PA"],
                           title="Minutes Played vs. FG% with Size = Effective FG%", hover_name="Name")

    st.plotly_chart(min_shots)

    st.write("""This chart depicts three major things: minutes per game, field goal percentage, and
    effective field goal percentage. The size of each bubble is  based on the effective FG%. This chart
    therefore depics offensive efficiency with respect to time played.""")

    st.write("""Some players jump out at us immediately. For example, Juan Toscano-Anderson, who has 
    an FG% of 0.585 on 20.5 minutes played per game. Juan also shoots the 3 at around 41%, which only 
    a few other players on the team can do. Outside of the regular starter, Juan is probably the most
    impactful on offense, averaging 2.7 assists per game as well, which is third-highest on the team. 
    This is significant primarily because Juan was not a regular on the team till this season, yet has shown
    his worth to the Warriors. James Wiseman is another player with similar production, but he is currently
    injured. However, as a rookie Wiseman has also shown flashes of brilliance, averaging 11.5 PPG on 21.4 minutes
    per game, with both his FG% and eFG% above 50. These two players will hopefully be major parts of the 
    Warriors team in the seasons to come.""")

    st.write("""The most striking anomaly here, however, is Gary Payton II. While he has only played 10
    games, he has averaged 2.5 PPG on 4 minutes per game, with a 3P% of 50% and an eFG% of 85%! This 
    makes a good case for Payton II receiving more minutes and hopefully continuing to produce
    as he has in the opportunities he has received this season.""")

    st.subheader("Defensive Stalwarts")

    blocks_fouls = px.scatter(per_game, x="STL", y="BLK", size="PF", hover_name="Name", 
                              title="Blocks vs. Steals, Size = Personal Fouls",
                              hover_data=["MP", "G"])

    st.plotly_chart(blocks_fouls)

    st.write("""This chart shows important defensive measures – steals vs. blocks with bubble size
    as the number of personal fouls per game. It's good if your block and steal numbers are high – it's
    even better if you can get those high numbers with fouling too much on average. This chart clearly shows
    that the Warriors' defensive master is Draymond Green, who averages 1.7 steals and 0.8 blocks per game.""")
    
    st.write("""These may not seem like large numbers, but often defensive efforts do not always show up on the stats
    sheet. The measures that do, however, tell us about how often a player can disrupt an opponent's
    offensive possession. Andrew Wiggins is another important defensive player for the Warriors – he averages
    a higher block rate than Green, along with a lower foul rate. Wiggins and Green are the players who most
    often guard the opponent's main offensive player – they are the Warriors' defensive stalwarts, and part of
    the reason the Warriors are 5th in the league in defensive rating.""")

    st.subheader("Draymond Green: Point Forward")

    ast_tov = px.scatter(per_game, x="AST", y="TOV", size="DRB", hover_name="Name", 
                         title="Assists vs. Turnovers, Size = Defensive Rebounds")

    st.plotly_chart(ast_tov)

    st.write("""Assists are an important part of offensive production, and making the most of an 
    offensive possessions requires passing the ball to the person most likely to score, without
    turning the ball over to the other team too much. This chart shows that Draymond Green and Steph
    Curry have been the two players most capable of efficiently assisting their fellow teammates this
    season. For Green, this 'point forward' position is his main role on this team – 
    to coordinate the offense and provide good looks for his teammates. 
    A large part of the reason Curry is able to put on the offensive
    shows he does is because Green is there to run the offense and take the attention off of Curry, 
    who can then shake his defender and get the ball from Green in order to score. """)

if viz_select == "Per 100 Possessions":

    st.sidebar.write("""The Per 100 Posessions tab provides inferences based on the players'
    averages across all the major stats per 100 possessions. This gives a broader view
    of team trends.""")

    st.header("GSW 2020-21 Per 100 Possessions Stats")

    per_100_poss_h_m = per_100_poss.style.background_gradient(cmap='viridis')

    st.write(per_100_poss_h_m)

    st.write("""The data frame above is formatted based on which values are outliers compared to the average
    over the range of values that each column takes. This helps to quickly identify statistical outliers,
    especially among those who are lower down in the table. One such example is Alen Smailagić, who,
    while only playing 64 minutes per 100 possessions, averages 3.7 blocks per 100 possessions, a team high!
    Such insights are important when judging the value of role-players coming off the bench.""")

    st.header("Per 100 Possessions Analytics and Inferences")

    st.subheader("Offensive and Defensive Ratings")

    st.write("""Offensive and Defensive Ratings tell us how many points a player produces and gives up
                respectively. Therefore, per 100 possession, ORTG and DRTG can be illuminating, especially
                in terms of defense. While you may not get a block or a steal, if you play good enough
                defense, the player you're guarding will miss their shot, and this defensive
                effort will show up in the DRTG. So it's worth taking a look at the ORTG and DRTG
                trends of the team.""")

    ortg_dtrg = px.density_heatmap(per_100_poss, x="ORTG", y="DRTG", 
                nbinsx=10, nbinsy=10, marginal_x="histogram",
                marginal_y="histogram", 
                title="Offensive Rating (ORTG) vs. Defensive Rating (DRTG) Heatmap")

    st.plotly_chart(ortg_dtrg)

    st.write("""In the graph above, we can see that most players on the team fall in the range of
                110-114 DRTG and 100-109 ORTG. This is shown by the distribution graphs on either
                axes – this is helpful in quickly seeing macro trends in the team's ratings distribution.
                What these distributions also show us is there is quite a bit of variation in ORTG and 
                DRTG – Warriors players generally tend to have higher ORTG and average DRTG. It's important
                to remember that with DRTG, the lower, the better. You want to be giving up less points
                per 100 possessions, not more. The Warriors only have 2 players with DRTGs below 105, but
                they have 7 players with an ORTG above 110. However, the Warriors as a team
                are above average on defense, so this may not be such an issue. """)

    st.subheader("Ratings and More Tangible Stats")

    st.write("""One would assume that Points per 100 Possessions and Offensive Rating would be
                positively correlated – after all, the more points you score, the higher your 
                ORTG should be, right? """)

    ortg_pts = px.density_heatmap(per_100_poss, x="ORTG", y="PTS",
                nbinsx=15, nbinsy=15, color_continuous_scale="Viridis",
                title="ORTG vs. Points Heatmap")

    st.plotly_chart(ortg_pts)

    st.write("""The heatmap above does not seem to imply this. In fact, it seems to imply a weakly
                negative relationship between ORTG and Points. We can use a bubble scatter plot
                to see this relationship in a bit more detail.""")

    ortg_pts_scatter = px.scatter(per_100_poss, x="ORTG", y="PTS", hover_name="Player", size="G",
                                  trendline="ols", title="ORTG vs. Points, Size = Games",
                                  trendline_color_override="black")

    st.plotly_chart(ortg_pts_scatter)

    st.write("""This graph shows that there indeed seems to be a weakly negative relationship between
                ORTG and Points, but the outliers are significant. Steph Curry is far ahead of the rest
                of the team, averaging 43.8 points per 100 possessions with an ORTG of 119. While Gary
                Payton II is also an anomaly, I've added the size of the bubbles to be based
                on the number of games played. This allows us to contextualise which anomalies
                are significant and which may be inflated due to the lower number of games played.""")

    st.write("""The significance of the outliers is also noted in the OLS trendline, which is actually
                weakly positive. The low $R^{2}$ value indicates that the trendline is not a good fit
                to the data, so any relationship we may glean from just a glance at the data will not
                really give us a meaningful relationship. Still, it is interesting that there is 
                not a strong correlation between Points and ORTG.""")

    ast_ortg = px.scatter(per_100_poss, x="ORTG", y="FG%", size="G", 
                          hover_name="Player", trendline="ols",
                          title="ORTG vs. FG%, Size = Games", trendline_color_override='darkblue')

    st.plotly_chart(ast_ortg)

    st.write("""However, there is a much clearer correlation between ORTG and FG% (field goal percentage).
                This shows us that it's not exactly how much you score that matters to ORTG, it's
                how efficiently you score. Here, Steph Curry does not seem to be ahead of the pack
                here – Juan Toscano-Anderson and Kevon Looney seem to be, apart from Gary Payton II,
                who seems to be an anomaly pretty much everywhere. But this tells us about how much
                efficiency matters to a team at large.""")

    st.write("""Furthermore, if we were to check ORTG against
                effective FG% we would most likely see Curry and the other good three-point shooters
                stand out, since effective FG% adjusts for the fact that a three-pointer is worth more
                than a two-pointer. Unfortunately, eFG% is not calculated per 100 possessions, so
                we can only speculate. But this provides more than enough insight into larger
                offensive trends for the Warriors.""")

    pf_drtg = px.scatter(per_100_poss, x="DRTG", y="PF", size="G", hover_name="Player",
                         trendline="ols", title="DRTG vs. Personal Fouls, Size = Games",
                         trendline_color_override="red")


    st.plotly_chart(pf_drtg)

    st.write("""We can see in the chart above that there seems to be a fairly significant
                negative correlation between personal fouls and defensive rating. This could
                be because less talented defender are less likely to foul when playing on-ball
                defense, instead getting blown by and giving up a shot. Ideally, one would want
                both a low PF and DRTG. The closest player to that seems to be (surprise, surprise)
                Draymond Green, with a DRTG of 106 and a PF of 4.6 per 100 possession average. The fact that most of the Warriors
                are clustered at the far end of the DRTG axis may mean that personal defense will
                need to get better for the Warriors.""")

if viz_select == "Advanced":

    st.header("GSW 2020-21 Advanced Stats")

    advanced_hm = advanced.style.background_gradient(cmap='viridis')

    st.write(advanced_hm)

    st.write(""""The data frame above is formatted based on which values are outliers compared to the average
    over the range of values that each column takes. This helps to quickly identify statistical outliers,
    especially among those who are lower down in the table. One such example here is Mychal Mulder,
    who has a 3-Point Attempt Rate (% of FG attempts from 3-point range) of 0.809 – nearly 81% of his
    shot attempts are threes. Given that Mulder is 5th on the team in True Shooting Percentage (TS%),
    we can see that he is an effective three point shooter who is not afraid to shoot the three
    and in fact seems to look and/or settle for that shot most of the time.""")

    st.header("Advanced Analytics and Inferences")

    st.subheader("Variability and Outliers in Usage Rates")

    per_box = px.box(advanced, y="USG%", hover_name="Name", points="all")

    st.plotly_chart(per_box)

    st.write("""The chart above is a box plot on Usage Rate for the Warriors this season. Usage Rate is
    defined as the estimated percentage of team plays used by a player when they are on the floor. The box
    plot shows the max and min Usage Rate along with the 1st and 3rd Quartile and the Median. This is 
    useful for getting a quick overview of the variability in usage rate, which is an important statistic
    on a team that relies heavily on a few players.""")

    st.write("""Here, Steph Curry seems to be the only real outlier (Marquese Chriss was traded
    midway through the season, so we will not currently consider his contributions as we are looking
    for future team trends). Steph has the highest usage rate, but among the rest of the team,
    very few others come close. One might suspect that Draymond Green's usage rate would be higher
    given that the eye test indicates he coordinates many plays on the floor, but the box plot indicates
    he has one of the lowest usage rates – just 13.1%. Yet his assists percentage is the highest on the 
    team. But his offensive win shares are not high compared to the rest of the team – his defensive
    win shares top the team! This is quite bizarre for a player to have such a dominating offensive
    presence in one part of the stats sheet but not in the other.""")

    ws_usg = px.scatter(advanced, x="USG%", y="WS", hover_name="Name", size="G")

    st.plotly_chart(ws_usg)

    st.write("""The good old scatterplot is pretty useful in seeing just how useful Draymond is
    to this team. He is in the bottom five in usage rate but second highest in total win shares.
    His total win shares is contributed to mostly by his defense, even though his offense is clearly elite
    from his assist percentage. It's rare to find such a impactly player with low usage, and in fact, this
    could be a good reason for why Draymond can play well with Steph. Steph needs the ball in his hands, but
    he knows that the offense can run through Draymond if Curry needs to shake his defender off-ball. 
    This coupled with Draymond's unselfishness really brings out a brilliant 2-man dynamic to the Warriors,
    and this is only going to get harder for opponents to guard once Klay Thompson comes back.""")

    per_vorp = px.scatter(advanced, x="PER", y="VORP", hover_name="Name")

    st.plotly_chart(per_vorp)

    st.write("""The Player Efficiency Rating (PER) vs. Value over Replacement Player (VORP) also shows that
    as far as the Warriors Front Office is concerned, Curry and Green are the two most irreplaceable
    players on the team. But it also shows that Gary Payton II is underrated. We've seen that he is an
    anomaly in most other places, but his VORP is quite low. Does that mean that he is easily replaceable?
    Well, his PER is actually higher than Steph's, and the main reason his VORP is low is because
    VORP takes into account % of team possessions played by a single player. Since Payton II
    comes off the bench mostly in garbage time, his VORP will be low. But give him quality minutes
    in the play-in tournaments and playoffs, and we can expect his VORP to increase relative to his
    PER. The Warriors will need defense in the coming games, so players like Payton II and Green,
    along with Wiggins and Thompson when he returns, will be crucial.""")



    


# roster


# hm_roster

# Your League of Legends (LOL) champion counter assistant
This is program designed to find best champion counters given what champions the enemy team is hovering during cham-selection!

<p align="center">
  <img src="lol_logo.png" width="350" alt="LoL Logo">
</p>

## How do I run the app?

Simply type `python main.py` in the terminal, while making sure that your current working directory is the root of the project, and you have the required libraries installed. You can get required dependencies by running:

```bash
uv sync
```

And everything should be installed (I hope, I have not tested this yet, but it should work). Then, you just follow the prompts to input your role and the enemy champions, and the app will give you the top five highest scoring counters!

**Example:**

Here is an example, where I picked support (supp), and the enemy team is hovering nami, ahri, garen, lucian, and ivern:
```bash
Enter your role [top, jgl, mid, bot, supp]: supp
Enter enemy champions (comma separated): nami, ahri, garen, lucian, ivern

--- RESULTS ---

Your most probable lane opponent: Nami

Best picks:

Blitzcrank      | Score: 3.75
Leona           | Score: 2.71
Sona            | Score: 1.92
Akali           | Score: 1.47
Brand           | Score: 1.36
```



> [!IMPORTANT]
> For champion names with spaces, for instance, if the enemy is hovering Master Yi, just write masteryi! 

## How does it work?

1. Gameplay match data from the Riot API is retrieved and stored in a local CSV file. This data includes information about which champions are played, who they played against, their roles, and whether they won or lost.

2. From the data, we calculate the winrate and number of games played for each champion matchup in each role. 

3. When you run the app, you input your role and then the enemy champions. The app predicts who your enemy laner is and gives the top five highest scoring counters!

## How is the score calculated?

In the code, we defined:

```python
score = (winrate - 0.5) * sqrt(games)
```

So we only get a positive score if the winrate itself is above 50%, and it scales with the number of games to give more confidence to the counters.

**Example:**

If the app suggests katarina with a score of 2.5, it COULD mean:

$$
\text{winrate} = 0.65 \Rightarrow (0.65 - 0.5) = 0.15
$$
$$
\text{games} ≈ 280 \Rightarrow \sqrt{280} \approx 16.7
$$
$$
\text{score} ≈ 0.15 \cdot 16.7 \approx 2.5
$$

Basically, the higher the better, and if negative, it means the champion is actually a bad counter (winrate below 50%).

[!NOTE]
> ## Below is something very important that you must know about the data:

## Data requirements

This application does not include any preloaded match data. Due to Riot Games API policies, I could not include match data. Therefore, potential users like you must retrieve your own data using the Riot API before running the application.

> [!IMPORTANT]
> The model and recommendations are entirely based on the data you collect locally.

## How do I retrieve the data then?

To use this application, you must first collect match data yourself:

1. Go to the "Riot Developer Portal": [CLICK HERE](https://developer.riotgames.com/)
2. Sign in with your Riot account (I assume you have an account if you are reading this, but if not, you can create one)
3. Generate an API key

Create a `.env` file in the root of the project and add:

```python
MY_API_KEY = "your_api_key_here"
```

Then create an empty folder named `data` in the root of the project and then go the the `data_retriever.ipynb` notebook and run the cells to retrieve match data. The notebook is well commented and should be easy to follow (in my opintion at least). This will generate the required dataset (CSV files) locally!




> [!NOTE]
> * The quality of recommendations depends entirely on your dataset
> * Larger datasets will produce more reliable results
> * Data collection may take significant time due to API rate limits
>
> For reference, collecting data for around 1000 players and 3 matches each (so 3000 matches total) can take around 2 hours (121 minutes and 40 seconds for me), so be patient if you choose to collect a large dataset!



> [!IMPORTANT]
>
> Do not share or publish the collected dataset
> Keep your API key private at all times
> The `.env` file is ignored by Git to prevent accidental exposure

So maybe the beginning was a bit of a "bait", this program is not really ready to be used out of the box, but I hope that with some effort, you can get it up and running and find it useful!


<!-- > [!NOTE]
> ## Something you must know about the data:
> The app is "trained" on data from 1000 players and 3 matches per player (so a total of 3000 matches!), and all players are Emerald 1, so the counters are biased towards this skill level, AND some champions might be missing due to lack of data.
> 
> But you are welcome to run the data retrieval code yourself to get more data and update the counters if you want :), I couldn't and did not have the patiance to retrieve more. For reference, loading 1000 players and 3 matches per player took 121 minutes and 40 seconds so good luck.


> [!TIP]
> ## If you want to retrieve data yourself:
> <p align="center">
>  <img src="em.png" width="250" alt="emerald logo">
> </p>
>
> Go to this link:
>
> [click here](https://developer.riotgames.com/)
>
> And sign up with your Riot account (or create one, but I assume you play league if you are reading this). Then, you will be given an API key, which you must use. To use the API key, create a `.env` file in the root of the project and add the following line:
>
> ```python
> MY_API_KEY = "insert your API key here"
> ```
>
> Then, you can run the `data_retriever.ipynb` notebook to retrieve the data and save it to CSV files. The notebook is well commented (imo) and should be easy to follow, and the `.env` file is already ignored, so you don't have to worry about accidentally pushing your API key to GitHub. -->
# Pokemon Go Bot

## Setup
First, clone the repository: `git clone https://github.com/acmattson3/pogo-bot/`

Then, enter the repository (`cd pogo-bot`) and clone the image assets:

```
git clone --filter=blob:none --no-checkout https://github.com/PokeMiners/pogo_assets.git
cd pogo_assets
git sparse-checkout init --cone
git sparse-checkout set Images
git checkout
```

Then, optionally, create and enter a conda environment for the bot (requires anaconda) and install the dependencies:
```
conda env create -f environment.yml
conda activate pogo-bot
```
Or, just do it however you want!

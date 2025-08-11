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

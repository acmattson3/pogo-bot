"""
This module defines structured configuration data for interacting with the
Pokémon GO user interface via automated scripts. Rather than hard-coding
absolute pixel coordinates, each interactive element is represented by a
``Locator`` pointing at a template image stored in ``asset_dir``. When
matching on screen, the templates are compared using OpenCV with a
configurable threshold. Swipes are described using screen-percentage
coordinates so they scale across devices.  Signature rectangles are
expressed as fractions of the screen (x, y, w, h) and are used by the
application layer to detect when you've reached the end of a list (e.g.
when the CP/weight signatures no longer change after swiping).

The configuration is grouped into logical dataclasses. ``TopBarUI`` holds
references to the icons visible on the Map View, such as the weather
button, compass, Campfire, Daily Adventure Incense indicator, Today View,
Nearby, Main Menu, Buddy and Trainer icons【582666050288924†L22-L53】.

``WeatherMenuUI`` encapsulates the elements that appear when you tap
the weather icon and choose to report an issue. After tapping “Report
Weather Issue” the player is offered options like “The weather is not
accurate at all” or “The weather seems about, just not up to date” with
Submit and Cancel buttons【408654206636446†L160-L164】.  A third option
representing “Weather is accurate” is included for completeness even
though it may not currently be present.

``IncensePopupUI`` describes the pop-up that appears when the Daily
Adventure Incense is available. It typically offers “USE NOW” and
“MAYBE LATER” buttons【582666050288924†L43-L45】.

``ResearchMenuUI`` (also referred to as the Today View or Research View) models the
Research page accessed via the binoculars icon on the Map View.  The page
is divided into tabs labelled **Today**, **Special** and **Events** according to
Niantic's help documentation【32926885883476†L23-L84】.  The Today tab contains
daily and field research tasks, breakthrough stamps, PokéCoin/bonus
progress and event bonuses; the Special tab lists active and completed
Special Research campaigns; and the Events tab lists timed research,
collection challenges and passes【304336375535609†L459-L468】.  Additional
locators cover a **View Rewards** button used within event research chains,
the **Claim Rewards** button to collect the rewards and an **X** button to
close the pop-up.
According to the Pokémon GO wiki, the page is divided into three tabs -
Today, Special and Events.  The Today tab contains Field Research tasks,
Research Breakthrough stamp progress, daily PokéCoin and bonus progress,
and event bonuses; the Special tab lists active and completed Special
Research campaigns; the Events tab lists Timed Research campaigns,
Collection Challenges, GO Passes and future events【304336375535609†L459-L468】.
We also provide locators for the “View Rewards” pop-up used within
certain Event research chains and its “Claim Rewards” and close (X)
buttons as described by the user.

``NearbyMenuUI`` represents the Nearby menu (bottom-right binocular icon on
the Map View).  As of the RSVP planner update, the menu is split into
three high-level tabs — **Pokémon**, **Battle** and **Route**【785033708753621†L81-L84】.
Under **Battle** there are sub-tabs for **Raid**, **Power Spot** and **RSVP**
【785033708753621†L80-L84】.  The Pokémon tab itself contains “Nearby” and
“Sightings” sections showing wild Pokémon near PokéStops or in grass
【656802029251610†L430-L486】.  The Raid sub-tab further divides into local and
remote raid lists【656802029251610†L500-L512】, and the Power Spot tab splits into
sections for your MP meter and active Max Battles【656802029251610†L520-L532】.
The Route tab lists nearby route starting points and includes a button to
open the separate Routes view【656802029251610†L540-L544】.  Additional locators
cover the **Browse Campfire** button and a sorting button used in raid
lists, as well as the **RSVP** button for scheduling raids (when present)
【785033708753621†L91-L104】.

``AppraiseMenuUI`` contains elements used when inspecting Pokémon. A
hamburger icon (“three bars”) opens a context menu exposing the
Appraise, Tag and Transfer actions. Within the Appraise flow, one tap
advances through the IV star chart. If a Pokémon earns three stars,
another tap exits the appraisal and the script can tag it with the
“Three Star” tag. Locators are provided for the hamburger button, the
Appraise button, the Tag button, the specific “Three Star” tag,
the close (X) button on the tagging dialog and the badge used to
recognise three-star Pokémon.

``PokemonListUI`` offers anchors for the first Pokémon in the list and
buttons to change sorting (e.g. sort by CP or other criteria).  These
anchors help scripts reliably locate and interact with the list without
hard-coded coordinates.

``RoutesMenuUI`` includes elements of the separate Routes feature, such
as buttons to see nearby routes, create new routes or enter a share
code, and tabs for “All” and “Popular” within the Routes browser.  The
Nearby tab of the Nearby menu links here【630971746247901†L534-L544】.

Finally, ``UiPack`` bundles all the UI groups along with swipe
definitions, wait timings and signature rectangles. Call
``default_pack()`` to obtain a ready-to-use configuration using
standard asset names.  Adjust the file names and thresholds in the
default definition to match your own captured templates.
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Locator:
    """Represents an on-screen anchor image and its match threshold."""
    file: str
    thresh: float = 0.86


@dataclass(frozen=True)
class Swipe:
    """Defines a swipe gesture using start and end points in screen-percentage coordinates."""
    start: Tuple[float, float]
    end: Tuple[float, float]
    duration_ms: int = 280


@dataclass(frozen=True)
class SignatureRects:
    """Regions used to generate signatures for detecting end of lists (CP and weight)."""
    cp: Tuple[float, float, float, float]
    weight: Tuple[float, float, float, float]


@dataclass(frozen=True)
class TopBarUI:
    """Anchors for icons along the top of the Map View."""
    weather: Locator
    compass: Locator
    campfire: Locator
    bluetooth: Locator
    bonuses: Locator
    rocket_radar: Locator
    daily_incense: Locator
    today_view: Locator
    nearby: Locator
    main_menu: Locator
    buddy: Locator
    trainer: Locator


@dataclass(frozen=True)
class WeatherMenuUI:
    """Elements within the Weather menu and reporting flow."""
    report_issue: Locator
    option_not_accurate: Locator
    option_not_up_to_date: Locator
    option_accurate: Locator
    submit_button: Locator
    cancel_button: Locator


@dataclass(frozen=True)
class IncensePopupUI:
    """Buttons shown when the Daily Adventure Incense pop-up appears."""
    use_now: Locator
    maybe_later: Locator


@dataclass(frozen=True)
class ResearchMenuUI:
    """Tabs and buttons on the Research page."""
    tab_today: Locator
    tab_special: Locator
    tab_events: Locator
    events_view_rewards: Locator
    events_claim_rewards: Locator
    events_close: Locator


@dataclass(frozen=True)
class NearbyMenuUI:
    """The Nearby menu and its sub-tabs."""
    tab_pokemon: Locator
    tab_battle: Locator
    tab_route: Locator
    battle_tab_raid: Locator
    battle_tab_power_spot: Locator
    battle_tab_rsvp: Locator
    raid_browse_campfire: Locator
    raid_sort_button: Locator
    routes_tab_all: Locator
    routes_tab_popular: Locator
    rsvp_button: Locator


@dataclass(frozen=True)
class AppraiseMenuUI:
    """Locators used when appraising and tagging Pokémon."""
    three_bars: Locator
    appraise_btn: Locator
    tag_btn: Locator
    tag_three_star: Locator
    tag_close: Locator
    three_stars_badge: Locator


@dataclass(frozen=True)
class PokemonListUI:
    """Anchors and controls within the Pokémon list."""
    first_pokemon_anchor: Locator
    sort_button: Locator
    sort_by_cp: Locator
    sort_by_name: Locator
    sort_by_num: Locator
    sort_by_hp: Locator


@dataclass(frozen=True)
class RoutesMenuUI:
    """Locators for the Routes feature."""
    see_nearby_routes: Locator
    create_route: Locator
    enter_share_code: Locator
    tab_all: Locator
    tab_popular: Locator

@dataclass(frozen=True)
class MainMenuUI:
    """Buttons and sub-menus within the Main Menu (Pokéball icon).

    According to Niantic's Map View article, the Main Menu provides access
    to settings, news, your Item Bag, Pokédex, shop, battle menu and
    Pokémon inventory【809700503260562†L29-L53】.  Additional sites like
    Fev Games note that the main menu includes tabs for Items, Pokédex,
    Pokémon, Settings, Shop and Tips【836772960819126†screenshot】.  We include
    locators for all of these options so scripts can navigate the menu
    without hard-coded coordinates.
    """
    items: Locator
    pokedex: Locator
    pokemon: Locator
    shop: Locator
    news: Locator
    battle: Locator
    settings: Locator
    tips: Locator


@dataclass(frozen=True)
class CampfireMenuUI:
    """Tabs and controls within the Campfire overlay.

    The Campfire feature serves as Niantic's social and coordination
    platform.  While there is limited official documentation on its
    in-game categories, the user describes a tab menu containing
    categories such as **All**, **Meetups**, **Raids**, **G-MAX**, **D-MAX**,
    **Flares**, **Playgrounds** and **Routes**, along with a Filters
    button (visible when appropriate) and a List view button.  Locators
    for each tab and control are provided here.  If you don't use
    Campfire often, you may omit unused images.
    """
    tab_all: Locator
    tab_meetups: Locator
    tab_raids: Locator
    tab_gmax: Locator
    tab_dmax: Locator
    tab_flares: Locator
    tab_playgrounds: Locator
    tab_routes: Locator
    filters_button: Locator
    list_button: Locator


@dataclass(frozen=True)
class BattleMenuUI:
    """Options inside the Battle menu accessed from the Main Menu.

    The Battle menu hosts a variety of battle modes including the
    GO Battle League, trainer battles (via QR code or friends), battles
    against Team Leaders and the ability to manage battle parties.  The
    Niantic Battling Trainers article notes that you access these via
    Main Menu → Battle → Nearby Battle【643738839633796†L45-L49】.  These
    locators provide anchors for each option so automation can choose
    between them.
    """
    go_battle_league: Locator
    trainer_battle: Locator
    team_leaders: Locator
    nearby_battle: Locator
    battle_party: Locator


@dataclass(frozen=True)
class RoutesViewUI:
    """Controls and categories within the Routes View.

    When players tap **See Nearby Routes** from the Route tab of the
    Nearby menu, the Routes View opens.  The Pokémon GO wiki describes
    options to exit back to Map View, display a tutorial, center the
    map and toggle the compass【471738295262181†L450-L466】.  Trainers can expand
    the view to list routes and use a flag button to sort by categories
    such as **All**, **Known**, **Official**, **New** and **Popular**
    【471738295262181†L465-L475】.  From a specific Route view, they can
    preview start/end points and choose to **FOLLOW**, **PAUSE**, **RESUME**
    or **QUIT** the route【471738295262181†L477-L527】.  This dataclass
    encapsulates locators for these controls and categories.
    """
    close: Locator
    tutorial: Locator
    center: Locator
    compass: Locator
    sort_flag: Locator
    category_all: Locator
    category_known: Locator
    category_official: Locator
    category_new: Locator
    category_popular: Locator
    follow_button: Locator
    pause_button: Locator
    resume_button: Locator
    quit_button: Locator


@dataclass(frozen=True)
class Waits:
    """Default wait times (in seconds) after various actions."""
    after_launch: float = 8.0
    after_menu_open: float = 1.0
    after_list_open: float = 1.0
    after_open_detail: float = 0.7
    after_three_bars: float = 0.5
    after_open_appraise: float = 0.9
    after_tap_advance: float = 0.5
    after_tag_open: float = 0.5
    after_apply_tag: float = 0.4
    after_close_tag: float = 0.4
    after_swipe: float = 0.7


@dataclass(frozen=True)
class UiPack:
    """Container for all UI locators and timing information."""
    asset_dir: str
    top_bar: TopBarUI
    weather_menu: WeatherMenuUI
    incense_popup: IncensePopupUI
    research_menu: ResearchMenuUI
    nearby_menu: NearbyMenuUI
    main_menu: MainMenuUI
    campfire_menu: CampfireMenuUI
    battle_menu: BattleMenuUI
    appraise_menu: AppraiseMenuUI
    pokemon_list: PokemonListUI
    routes_menu: RoutesMenuUI
    routes_view: RoutesViewUI
    swipes: Dict[str, Swipe]
    waits: Waits
    sig_rects: SignatureRects


def default_pack(asset_dir: str = "./assets") -> UiPack:
    """Return a UiPack with placeholder template names and sensible defaults.

    Replace file names with your own captured assets and adjust thresholds as
    necessary. These names should correspond to PNG files stored under
    ``asset_dir``.  For example, ``weather_icon.png`` should contain a
    cropped screenshot of the weather icon on your device.  The
    ``swipes`` dictionary defines a single swipe gesture for moving to
    the next Pokémon; you can add additional gestures keyed by name.
    """
    return UiPack(
        asset_dir=asset_dir,
        top_bar=TopBarUI(
            weather=Locator("weather_icon.png"),
            compass=Locator("compass_icon.png"),
            campfire=Locator("campfire_icon.png"),
            bluetooth=Locator("bluetooth_icon.png"),
            bonuses=Locator("bonuses_icon.png"),
            rocket_radar=Locator("rocket_radar_icon.png"),
            daily_incense=Locator("daily_incense_icon.png"),
            today_view=Locator("today_view_icon.png"),
            nearby=Locator("nearby_icon.png"),
            main_menu=Locator("main_menu_icon.png"),
            buddy=Locator("buddy_icon.png"),
            trainer=Locator("trainer_icon.png"),
        ),
        weather_menu=WeatherMenuUI(
            report_issue=Locator("weather_report_button.png"),
            option_not_accurate=Locator("weather_option_not_accurate.png", 0.88),
            option_not_up_to_date=Locator("weather_option_not_up_to_date.png", 0.88),
            option_accurate=Locator("weather_option_accurate.png", 0.88),
            submit_button=Locator("weather_submit_button.png"),
            cancel_button=Locator("weather_cancel_button.png"),
        ),
        incense_popup=IncensePopupUI(
            use_now=Locator("incense_use_now.png"),
            maybe_later=Locator("incense_maybe_later.png"),
        ),
        research_menu=ResearchMenuUI(
            tab_today=Locator("research_tab_today.png"),
            tab_special=Locator("research_tab_special.png"),
            tab_events=Locator("research_tab_events.png"),
            events_view_rewards=Locator("events_view_rewards.png"),
            events_claim_rewards=Locator("events_claim_rewards.png"),
            events_close=Locator("events_close_button.png"),
        ),
        nearby_menu=NearbyMenuUI(
            tab_pokemon=Locator("nearby_tab_pokemon.png"),
            tab_battle=Locator("nearby_tab_battle.png"),
            tab_route=Locator("nearby_tab_route.png"),
            battle_tab_raid=Locator("battle_tab_raid.png"),
            battle_tab_power_spot=Locator("battle_tab_power_spot.png"),
            battle_tab_rsvp=Locator("battle_tab_rsvp.png"),
            raid_browse_campfire=Locator("raid_browse_campfire.png"),
            raid_sort_button=Locator("raid_sort_button.png"),
            routes_tab_all=Locator("routes_tab_all.png"),
            routes_tab_popular=Locator("routes_tab_popular.png"),
            rsvp_button=Locator("rsvp_button.png"),
        ),
        main_menu=MainMenuUI(
            items=Locator("main_menu_items.png"),
            pokedex=Locator("main_menu_pokedex.png"),
            pokemon=Locator("main_menu_pokemon.png"),
            shop=Locator("main_menu_shop.png"),
            news=Locator("main_menu_news.png"),
            battle=Locator("main_menu_battle.png"),
            settings=Locator("main_menu_settings.png"),
            tips=Locator("main_menu_tips.png"),
        ),
        campfire_menu=CampfireMenuUI(
            tab_all=Locator("campfire_tab_all.png"),
            tab_meetups=Locator("campfire_tab_meetups.png"),
            tab_raids=Locator("campfire_tab_raids.png"),
            tab_gmax=Locator("campfire_tab_gmax.png"),
            tab_dmax=Locator("campfire_tab_dmax.png"),
            tab_flares=Locator("campfire_tab_flares.png"),
            tab_playgrounds=Locator("campfire_tab_playgrounds.png"),
            tab_routes=Locator("campfire_tab_routes.png"),
            filters_button=Locator("campfire_filters_button.png"),
            list_button=Locator("campfire_list_button.png"),
        ),
        battle_menu=BattleMenuUI(
            go_battle_league=Locator("battle_menu_league.png"),
            trainer_battle=Locator("battle_menu_trainer.png"),
            team_leaders=Locator("battle_menu_team_leaders.png"),
            nearby_battle=Locator("battle_menu_nearby.png"),
            battle_party=Locator("battle_menu_party.png"),
        ),
        appraise_menu=AppraiseMenuUI(
            three_bars=Locator("hamburger_icon.png"),
            appraise_btn=Locator("appraise_button.png"),
            tag_btn=Locator("tag_button.png"),
            tag_three_star=Locator("tag_three_star.png"),
            tag_close=Locator("tag_close.png"),
            three_stars_badge=Locator("three_stars_badge.png", 0.88),
        ),
        pokemon_list=PokemonListUI(
            first_pokemon_anchor=Locator("first_pokemon_anchor.png"),
            sort_button=Locator("sort_button.png"),
            sort_by_cp=Locator("sort_by_cp.png"),
            sort_by_name=Locator("sort_by_name.png"),
            sort_by_num=Locator("sort_by_num.png"),
            sort_by_hp=Locator("sort_by_hp.png"),
        ),
        routes_menu=RoutesMenuUI(
            see_nearby_routes=Locator("see_nearby_routes_button.png"),
            create_route=Locator("create_route_button.png"),
            enter_share_code=Locator("enter_share_code_button.png"),
            tab_all=Locator("routes_view_tab_all.png"),
            tab_popular=Locator("routes_view_tab_popular.png"),
        ),
        routes_view=RoutesViewUI(
            close=Locator("routes_view_close.png"),
            tutorial=Locator("routes_view_tutorial.png"),
            center=Locator("routes_view_center.png"),
            compass=Locator("routes_view_compass.png"),
            sort_flag=Locator("routes_view_sort_flag.png"),
            category_all=Locator("routes_view_category_all.png"),
            category_known=Locator("routes_view_category_known.png"),
            category_official=Locator("routes_view_category_official.png"),
            category_new=Locator("routes_view_category_new.png"),
            category_popular=Locator("routes_view_category_popular.png"),
            follow_button=Locator("routes_view_follow_button.png"),
            pause_button=Locator("routes_view_pause_button.png"),
            resume_button=Locator("routes_view_resume_button.png"),
            quit_button=Locator("routes_view_quit_button.png"),
        ),
        swipes={
            "next_pokemon": Swipe(start=(0.85, 0.50), end=(0.20, 0.50), duration_ms=280),
        },
        waits=Waits(),
        sig_rects=SignatureRects(
            cp=(0.42, 0.09, 0.22, 0.06),
            weight=(0.33, 0.62, 0.42, 0.08),
        ),
    )
